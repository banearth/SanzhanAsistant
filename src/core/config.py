from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - import-time guidance
    raise RuntimeError(
        "PyYAML is required to load config files. Install dependencies first, for example: pip install -e ."
    ) from exc


@dataclass(slots=True)
class AppConfig:
    default: dict[str, Any]
    tasks: dict[str, Any]
    safety: dict[str, Any]

    @property
    def runtime(self) -> dict[str, Any]:
        return self.default.get("runtime", {})


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping in {path}, got {type(data).__name__}")
    return data


def load_app_config(config_dir: Path) -> AppConfig:
    return AppConfig(
        default=_load_yaml(config_dir / "default.yaml"),
        tasks=_load_yaml(config_dir / "tasks.yaml"),
        safety=_load_yaml(config_dir / "safety.yaml"),
    )
