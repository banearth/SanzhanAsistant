from __future__ import annotations

from dataclasses import dataclass

from src.core.runtime import RuntimeContext


@dataclass(slots=True)
class DeviceHealth:
    controller_type: str
    serial: str
    is_ready: bool
    note: str


class DeviceAdapter:
    def __init__(self, ctx: RuntimeContext) -> None:
        self._ctx = ctx

    def health_check(self) -> DeviceHealth:
        device_cfg = self._ctx.config.device
        controller_type = str(device_cfg.get("type", "unknown"))
        serial = str(device_cfg.get("serial", "unset"))
        return DeviceHealth(
            controller_type=controller_type,
            serial=serial,
            is_ready=False,
            note="Controller integration is not wired yet. This adapter is a placeholder for future ADB/Win32 support.",
        )
