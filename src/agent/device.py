from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess

from src.core.runtime import RuntimeContext


@dataclass(slots=True)
class DeviceHealth:
    controller_type: str
    serial: str
    is_ready: bool
    note: str


@dataclass(slots=True)
class DeviceEntry:
    serial: str
    status: str


@dataclass(slots=True)
class DeviceProbe:
    serial: str
    screen_size: str
    resumed_activity: str
    package_name: str


class DeviceAdapter:
    def __init__(self, ctx: RuntimeContext) -> None:
        self._ctx = ctx

    @property
    def adb_path(self) -> str:
        return str(self._ctx.config.device.get("adb_path", "adb"))

    @property
    def target_serial(self) -> str:
        return str(self._ctx.config.device.get("serial", ""))

    def health_check(self) -> DeviceHealth:
        device_cfg = self._ctx.config.device
        controller_type = str(device_cfg.get("type", "unknown"))
        serial = str(device_cfg.get("serial", "unset"))
        devices = self.list_devices(connect_if_needed=True)
        matched = any(device.serial == serial and device.status == "device" for device in devices)
        if matched:
            note = "ADB device is reachable and matches the configured serial."
        elif devices:
            device_summary = ", ".join(f"{device.serial}({device.status})" for device in devices)
            note = f"Configured serial was not matched. Visible ADB devices: {device_summary}"
        else:
            note = "No ADB device is currently visible. Ensure MuMu is running and ADB is connected."
        return DeviceHealth(
            controller_type=controller_type,
            serial=serial,
            is_ready=matched,
            note=note,
        )

    def list_devices(self, connect_if_needed: bool = False) -> list[DeviceEntry]:
        if connect_if_needed and self.target_serial:
            self._connect(self.target_serial)

        result = self._run(["devices"], text=True)
        devices: list[DeviceEntry] = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if not line or line.startswith("List of devices attached"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                devices.append(DeviceEntry(serial=parts[0], status=parts[1]))
        return devices

    def probe(self) -> DeviceProbe:
        serial = self.target_serial
        self._connect(serial)
        screen_size_output = self._run(["-s", serial, "shell", "wm", "size"], text=True).stdout.strip()
        resumed_output = self._run(
            ["-s", serial, "shell", "dumpsys", "activity", "activities"],
            text=True,
            timeout=30,
        ).stdout
        resumed_activity = self._extract_resumed_activity(resumed_output)
        package_name = resumed_activity.split("/")[0] if "/" in resumed_activity else self._ctx.config.game.get("package_name", "")
        return DeviceProbe(
            serial=serial,
            screen_size=screen_size_output or "unknown",
            resumed_activity=resumed_activity or "unknown",
            package_name=str(package_name),
        )

    def capture_screenshot(self, output_path: Path) -> Path:
        serial = self.target_serial
        self._connect(serial)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        remote_path = "/sdcard/sanzhan_capture.png"
        self._run(["-s", serial, "shell", "screencap", "-p", remote_path], text=True)
        self._run(["-s", serial, "pull", remote_path, str(output_path)], text=True, timeout=30)
        self._run(["-s", serial, "shell", "rm", remote_path], text=True)
        return output_path

    def _connect(self, serial: str) -> None:
        if not serial or ":" not in serial:
            return
        self._run(["connect", serial], text=True, check=False)

    def _run(
        self,
        args: list[str],
        *,
        text: bool,
        timeout: int = 20,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
        command = [self.adb_path, *args]
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=text,
            timeout=timeout,
        )
        if check and completed.returncode != 0:
            stderr = completed.stderr if text else completed.stderr.decode("utf-8", errors="replace")
            raise RuntimeError(f"ADB command failed: {' '.join(command)}\n{stderr.strip()}")
        return completed

    def _extract_resumed_activity(self, dumpsys_output: str) -> str:
        match = re.search(r"(?:topResumedActivity|ResumedActivity): .*? ([^ ]+/[^ ]+) ", dumpsys_output)
        if match:
            return match.group(1)
        return ""
