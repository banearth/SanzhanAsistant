from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib
from typing import Any


@dataclass(slots=True)
class AppConfig:
    default: dict[str, Any]
    tasks: dict[str, Any]
    safety: dict[str, Any]
    teams: dict[str, Any]
    config_dir: Path

    @property
    def runtime(self) -> dict[str, Any]:
        return self.default.get("runtime", {})

    @property
    def device(self) -> dict[str, Any]:
        return self.default.get("device", {})

    @property
    def game(self) -> dict[str, Any]:
        return self.default.get("game", {})

    @property
    def planner(self) -> dict[str, Any]:
        return self.default.get("planner", {})

    @property
    def team_policy(self) -> dict[str, Any]:
        return self.teams


def _load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as file:
        data = tomllib.load(file) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping in {path}, got {type(data).__name__}")
    return data


def load_app_config(config_dir: Path) -> AppConfig:
    return AppConfig(
        default=_load_toml(config_dir / "default.toml"),
        tasks=_load_toml(config_dir / "tasks.toml"),
        safety=_load_toml(config_dir / "safety.toml"),
        teams=_load_toml(config_dir / "teams.toml"),
        config_dir=config_dir,
    )
