from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.core.config import AppConfig


@dataclass(slots=True)
class RuntimeContext:
    root_dir: Path
    config: AppConfig

    @property
    def fixture_dir(self) -> Path:
        return self.root_dir / "tests" / "fixtures"

    @property
    def report_dir(self) -> Path:
        relative = self.config.runtime.get("report_dir", "reports/daily")
        path = self.root_dir / relative
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def screenshot_dir(self) -> Path:
        relative = self.config.runtime.get("screenshot_dir", "reports/screenshots")
        path = self.root_dir / relative
        path.mkdir(parents=True, exist_ok=True)
        return path
