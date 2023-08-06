# -*- coding: utf-8 -*-
#
# Copyright 2019 SoloKeys Developers
#
# Licensed under the Apache License, Version 2.0, <LICENSE-APACHE or
# http://apache.org/licenses/LICENSE-2.0> or the MIT license <LICENSE-MIT or
# http://opensource.org/licenses/MIT>, at your option. This file may not be
# copied, modified, or distributed except according to those terms.

import base64
import binascii
import hashlib
import json
import secrets
import struct
import sys
import tempfile
import time
from getpass import getpass
from typing import Any, Optional

from fido2.client import Fido2Client, UserInteraction
from fido2.ctap import CtapError
from fido2.ctap1 import Ctap1
from fido2.ctap2 import CredentialManagement, Ctap2
from fido2.ctap2.pin import ClientPin
from fido2.hid import CTAPHID, CtapHidDevice, open_device
from intelhex import IntelHex

import pynitrokey.exceptions
import pynitrokey.fido2 as nkfido2
from pynitrokey import helpers
from pynitrokey.fido2.commands import SoloBootloader, SoloExtension
from pynitrokey.helpers import local_critical, local_print


class CliOrProvidedInteraction(UserInteraction):
    def __init__(self, pin: Optional[str]) -> None:
        self.pin = pin

    def prompt_up(self) -> None:
        print("Touch your authenticator device now...")

    def request_pin(self, permissions: Any, rd_id: Any) -> str:
        if self.pin:
            return self.pin
        else:
            return getpass("Enter PIN: ")

    def request_uv(self, permissions: Any, rd_id: Any) -> bool:
        return True


class NKFido2Client:
    def __init__(
        self,
    ):
        self.origin = "https://example.org"
        self.host = "example.org"
        self.user_id = b"they"
        self.exchange = self.exchange_hid
        self.do_reboot = True

    def use_u2f(
        self,
    ):
        self.exchange = self.exchange_u2f

    def use_hid(
        self,
    ):
        self.exchange = self.exchange_hid

    def set_reboot(self, val):
        """option to reboot after programming"""
        self.do_reboot = val

    def reboot(
        self,
    ):
        """option to reboot after programming"""
        try:
            self.exchange(SoloBootloader.reboot)
        except OSError:
            pass

    def find_device(self, dev=None, solo_serial: Optional[str] = None, pin=None):
        devices = []
        if dev is None:
            if solo_serial is not None:
                if solo_serial.startswith("device="):
                    solo_serial = solo_serial.split("=")[1]
                    dev = open_device(solo_serial)
                else:
                    devices = list(CtapHidDevice.list_devices())
                    devices = [
                        d for d in devices if d.descriptor.serial_number == solo_serial
                    ]
            else:
                devices = list(CtapHidDevice.list_devices())
            if len(devices) > 1:
                raise pynitrokey.exceptions.NonUniqueDeviceError
            if len(devices) > 0:
                dev = devices[0]
        if dev is None:
            raise RuntimeError("No FIDO device found")
        self.dev = dev

        self.ctap1 = Ctap1(dev)

        try:
            self.ctap2: Optional[Ctap2] = Ctap2(dev)
        except CtapError as e:
            self.ctap2 = None

        try:
            self.client: Optional[Fido2Client] = Fido2Client(
                dev, self.origin, user_interaction=CliOrProvidedInteraction(pin)
            )
        except CtapError:
            print("Not using FIDO2 interface.")
            self.client = None

        if self.exchange == self.exchange_hid:
            self.send_data_hid(CTAPHID.INIT, "\x11\x11\x11\x11\x11\x11\x11\x11")

        return self.dev

    @staticmethod
    def format_request(cmd, addr=0, data=b"A" * 16):
        # not sure why this is here?
        # arr = b"\x00" * 9
        addr = struct.pack("<L", addr)
        cmd = struct.pack("B", cmd)
        length = struct.pack(">H", len(data))

        return cmd + addr[:3] + SoloBootloader.TAG + length + data

    def send_only_hid(self, cmd, data):
        if not isinstance(data, bytes):
            data = struct.pack("%dB" % len(data), *[ord(x) for x in data])
        self.dev._dev.InternalSend(0x80 | cmd, bytearray(data))

    def send_data_hid(self, cmd, data):
        if not isinstance(data, bytes):
            data = struct.pack("%dB" % len(data), *[ord(x) for x in data])
        with helpers.Timeout(1.0) as event:
            return self.dev.call(cmd, data, event)

    def exchange_hid(self, cmd, addr=0, data=b"A" * 16):
        req = NKFido2Client.format_request(cmd, addr, data)

        data = self.send_data_hid(SoloBootloader.HIDCommandBoot, req)

        ret = data[0]
        if ret != CtapError.ERR.SUCCESS:
            raise CtapError(ret)

        return data[1:]

    def exchange_u2f(self, cmd, addr=0, data=b"A" * 16):
        appid = b"A" * 32
        chal = b"B" * 32

        req = NKFido2Client.format_request(cmd, addr, data)

        res = self.ctap1.authenticate(chal, appid, req)

        ret = res.signature[0]
        if ret != CtapError.ERR.SUCCESS:
            raise CtapError(ret)

        return res.signature[1:]

    def exchange_fido2(self, cmd, addr=0, data=b"A" * 16):
        chal = b"B" * 32

        req = NKFido2Client.format_request(cmd, addr, data)

        assertion = self.ctap2.get_assertion(
            self.host, chal, [{"id": req, "type": "public-key"}]
        )

        res = assertion
        ret = res.signature[0]
        if ret != CtapError.ERR.SUCCESS:
            raise RuntimeError("Device returned non-success code %02x" % (ret,))

        return res.signature[1:]

    def bootloader_version(
        self,
    ):
        data = self.exchange(SoloBootloader.version)
        if len(data) > 2:
            return (data[0], data[1], data[2])
        return (0, 0, data[0])

    def solo_version(
        self,
    ):
        try:
            return self.send_data_hid(0x61, b"")
        except CtapError:
            data = self.exchange(SoloExtension.version)
            return (data[0], data[1], data[2])

    def write_flash(self, addr, data):
        self.exchange(SoloBootloader.write, addr, data)

    def boot_pubkey(self):
        return self.exchange(SoloBootloader.boot_pubkey)

    def get_rng(self, num=0):
        ret = self.send_data_hid(SoloBootloader.HIDCommandRNG, struct.pack("B", num))
        return ret

    def get_status(self, num=0):
        ret = self.send_data_hid(SoloBootloader.HIDCommandStatus, struct.pack("B", num))
        # print(ret[:8])
        return ret

    def verify_flash(self, sig):
        """
        Tells device to check signature against application.  If it passes,
        the application will boot.
        Exception raises if signature fails.
        """
        self.exchange(SoloBootloader.done, 0, sig)

    def wink(
        self,
    ):
        self.send_data_hid(CTAPHID.WINK, b"")

    def reset(
        self,
    ):
        self.ctap2.reset()

    def make_credential(
        self,
        host="nitrokeys.dev",
        user_id="they",
        serial=None,
        output=True,
        udp=False,
        fingerprint_only=False,
    ):
        """
        fingerprint_only bool Return sha256 digest of the certificate, in a hex string format. Useful for detecting
            device's model and firmware.
        """

        user_id = user_id.encode()
        client = self.client

        rp = {"id": host, "name": "Example RP"}
        client.host = host
        client.origin = f"https://{client.host}"
        client.user_id = user_id
        user = {"id": user_id, "name": "A. User"}
        challenge = secrets.token_bytes(32)

        attestation_object = client.make_credential(
            {
                "rp": rp,
                "user": user,
                "challenge": challenge,
                "pubKeyCredParams": [
                    {"type": "public-key", "alg": -8},
                    {"type": "public-key", "alg": -7},
                ],
                "extensions": {"hmacCreateSecret": True},
            },
        ).attestation_object

        if fingerprint_only:
            if "x5c" not in attestation_object.att_stmt:
                raise ValueError("No x5c information available")
            from hashlib import sha256

            data = attestation_object.att_stmt["x5c"]
            return sha256(data[0]).digest().hex()

        credential = attestation_object.auth_data.credential_data
        credential_id = credential.credential_id
        if output:
            print(credential_id.hex())

        return credential_id

    def simple_secret(
        self,
        credential_id,
        secret_input,
        host="nitrokeys.dev",
        user_id="they",
        serial=None,
        pin=None,
        prompt="Touch your authenticator to generate a response...",
        output=True,
        udp=False,
    ):
        user_id = user_id.encode()

        client = self.client

        # rp = {"id": host, "name": "Example RP"}
        client.host = host
        client.origin = f"https://{client.host}"
        client.user_id = user_id
        # user = {"id": user_id, "name": "A. User"}
        credential_id = binascii.a2b_hex(credential_id)

        allow_list = [{"type": "public-key", "id": credential_id}]

        challenge = secrets.token_bytes(32)

        h = hashlib.sha256()
        h.update(secret_input.encode())
        salt = h.digest()

        if prompt:
            print(prompt)

        assertion = client.get_assertion(
            {
                "rpId": host,
                "challenge": challenge,
                "allowCredentials": allow_list,
                "extensions": {"hmacGetSecret": {"salt1": salt}},
            },
            pin=pin,
        ).get_response(0)

        output = assertion.extension_results["hmacGetSecret"]["output1"]
        if output:
            print(output.hex())

        return output

    def cred_mgmt(self, serial, pin):
        device = nkfido2.find(serial)
        client_pin = ClientPin(device.ctap2)

        try:
            client_token = client_pin.get_pin_token(pin)
        except CtapError as error:
            if error.code == CtapError.ERR.PIN_NOT_SET:
                local_critical("Please set a pin in order to manage credentials")
            if error.code == CtapError.ERR.PIN_AUTH_BLOCKED:
                local_critical(
                    "Pin authentication has been blocked, try reinserting the key or setting a pin if none is set"
                )
            if error.code == CtapError.ERR.PIN_BLOCKED:
                local_critical(
                    "Your device has been blocked after too many failed unlock attempts, to fix this it "
                    "will have to be reset. (If no pin is set, plugging it in again might fix this warning)"
                )
            raise

        return CredentialManagement(device.ctap2, client_pin.protocol, client_token)

    def enter_solo_bootloader(
        self,
    ):
        """
        If Nitrokey is configured as Nitrokey hacker or something similar,
        this command will tell the token to boot directly to the bootloader
        so it can be reprogrammed
        """
        if self.exchange != self.exchange_hid:
            self.send_data_hid(CTAPHID.INIT, "\x11\x11\x11\x11\x11\x11\x11\x11")
        self.send_data_hid(SoloBootloader.HIDCommandEnterBoot, "")

    def enter_bootloader_or_die(self):
        try:
            self.enter_solo_bootloader()
        # except OSError:
        #     pass
        except CtapError as e:
            if e.code == CtapError.ERR.INVALID_COMMAND:
                print(
                    "Could not switch into bootloader mode.  Please hold down the button for 2s while you plug token in."
                )
                sys.exit(1)
            else:
                raise (e)

    def is_solo_bootloader(
        self,
    ):
        try:
            self.bootloader_version()
            return True
        except CtapError as e:
            if e.code == CtapError.ERR.INVALID_COMMAND:
                pass
            else:
                raise (e)
        except Exception as e:
            # exception during bootloader version check, assume no bootloader
            # local_print("could not get bootloader version")
            pass
        return False

    def enter_st_dfu(
        self,
    ):
        """
        If Nitrokey is configured as Nitrokey hacker or something similar,
        this command will tell the token to boot directly to the st DFU
        so it can be reprogrammed.  Warning, you could brick your device.
        """
        soloboot = self.is_solo_bootloader()

        if soloboot or self.exchange == self.exchange_u2f:
            req = NKFido2Client.format_request(SoloBootloader.st_dfu)
            self.send_only_hid(SoloBootloader.HIDCommandBoot, req)
        else:
            self.send_only_hid(SoloBootloader.HIDCommandEnterSTBoot, "")

    def disable_solo_bootloader(
        self,
    ):
        """
        Disables the Nitrokey bootloader.  Only do this if you want to void the possibility
        of any updates.
        If you've started from a Nitrokey hacker, make you you've programmed a final/production build!
        """
        ret = self.exchange(
            SoloBootloader.disable, 0, b"\xcd\xde\xba\xaa"
        )  # magic number
        if ret[0] != CtapError.ERR.SUCCESS:
            print("Failed to disable bootloader")
            return False
        time.sleep(0.1)
        self.exchange(SoloBootloader.do_reboot)
        return True

    def program_file(self, name):
        def parseField(f):
            return base64.b64decode(helpers.from_websafe(f).encode())

        def isCorrectVersion(current, target):
            """current is tuple (x,y,z).  target is string '>=x.y.z'.
            Return True if current satisfies the target expression.
            """
            if "=" in target:
                target = target.split("=")
                assert target[0] in [">", "<"]
                target_num = [int(x) for x in target[1].split(".")]
                assert len(target_num) == 3
                comp = target[0] + "="
            else:
                assert target[0] in [">", "<"]
                target_num = [int(x) for x in target[1:].split(".")]
                comp = target[0]
            target_num = (
                (target_num[0] << 16) | (target_num[1] << 8) | (target_num[2] << 0)
            )
            current_num = (current[0] << 16) | (current[1] << 8) | (current[2] << 0)
            return eval(str(current_num) + comp + str(target_num))

        firmware_file_data = None
        if name.lower().endswith(".json"):
            firmware_file_data = json.loads(open(name, "r").read())
            fw = parseField(firmware_file_data["firmware"])
            sig = None

            if "versions" in firmware_file_data:
                current = (0, 0, 0)
                try:
                    current = self.bootloader_version()
                except CtapError as e:
                    if e.code == CtapError.ERR.INVALID_COMMAND:
                        pass
                    else:
                        raise (e)
                # for v in firmware_file_data["versions"]:
                #     if not isCorrectVersion(current, v):
                #         print("using signature version", v)
                #         sig = parseField(firmware_file_data["versions"][v]["signature"])
                #         break
                sig = parseField(firmware_file_data["versions"][">2.5.3"]["signature"])

                if sig is None:
                    raise RuntimeError(
                        "Improperly formatted firmware file.  Could not match version."
                    )
            else:
                sig = parseField(firmware_file_data["signature"])

            ih = IntelHex()
            tmp = tempfile.NamedTemporaryFile(delete=False)
            tmp.write(fw)
            tmp.seek(0)
            tmp.close()
            ih.fromfile(tmp.name, format="hex")
        else:
            if not name.lower().endswith(".hex"):
                print('Warning, assuming "%s" is an Intel Hex file.' % name)
            sig = None
            ih = IntelHex()
            ih.fromfile(name, format="hex")

        if self.exchange == self.exchange_hid:
            chunk = 2048
        else:
            chunk = 240

        seg = ih.segments()[0]
        size = seg[1] - seg[0]
        total = 0
        t1 = time.time() * 1000
        print("erasing firmware...")
        for i in range(seg[0], seg[1], chunk):
            s = i
            e = min(i + chunk, seg[1])  # type: ignore
            data = ih.tobinarray(start=i, size=e - s)
            self.write_flash(i, data)
            total += chunk
            progress = total / float(size) * 100
            sys.stdout.write("updating firmware %.2f%%...\r" % progress)
        sys.stdout.write("updated firmware 100%             \r\n")
        t2 = time.time() * 1000
        print("time: %.2f s" % ((t2 - t1) / 1000.0))

        if sig is None:
            sig = b"A" * 64

        success = False
        if self.do_reboot:
            try:
                print("bootloader is verifying signature...")
                print(f"Trying with {sig.hex()}")
                self.verify_flash(sig)
                print("...pass!")
                success = True
            except CtapError as e:
                if e.code != 0x27:
                    raise
                print("...error!")

        if not success:
            msg = """Bootloader reports failure in the signature verification. If your device is staying in the
            bootloader mode after reinserting it into the USB port, please execute the following to make it work again:

            # Download the compressed firmware file for Nitrokey FIDO2 128 v2.4.1 and extract it
            wget https://github.com/Nitrokey/nitrokey-fido2-firmware/releases/download/2.4.1.nitrokey/nitrokey-fido2-firmware-2.4.1-128kB-app-signed.zip
            unzip nitrokey-fido2-firmware-2.4.1-128kB-app-signed.zip
            # Run the update process again with the just downloaded firmware
            nitropy fido2 util program bootloader nitrokey-fido2-firmware-2.4.1-128kB-app-signed.json
            """
            local_critical(msg, support_hint=False)

        return sig

    def check_only(self, name):
        # FIXME refactor
        # copy from program_file
        if name.lower().endswith(".json"):
            data = json.loads(open(name, "r").read())
            fw = base64.b64decode(helpers.from_websafe(data["firmware"]).encode())
            sig = base64.b64decode(helpers.from_websafe(data["signature"]).encode())
            ih = IntelHex()
            tmp = tempfile.NamedTemporaryFile(delete=False)
            tmp.write(fw)
            tmp.seek(0)
            tmp.close()
            ih.fromfile(tmp.name, format="hex")
        else:
            if not name.lower().endswith(".hex"):
                print('Warning, assuming "%s" is an Intel Hex file.' % name)
            sig = None
            ih = IntelHex()
            ih.fromfile(name, format="hex")

        if sig is None:
            sig = b"A" * 64

        if self.do_reboot:
            self.verify_flash(sig)
