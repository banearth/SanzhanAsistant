from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from src.core.config import AppConfig


class TeamRole(str, Enum):
    MAIN_FORCE = "main_force"
    HARASS = "harass"


class DeploymentPolicy(str, Enum):
    FULL = "full"
    FIXED_SPLIT = "fixed_split"


@dataclass(frozen=True, slots=True)
class TeamPolicy:
    slot: int
    name: str
    role: TeamRole
    enabled: bool
    deployment_policy: DeploymentPolicy
    fixed_troops: tuple[int, ...] = ()
    exact_required: bool = False
    skip_if_insufficient: bool = True
    notes: str = ""

    @property
    def desired_total(self) -> int | None:
        if not self.fixed_troops:
            return None
        return sum(self.fixed_troops)

    def describe(self) -> str:
        if self.deployment_policy == DeploymentPolicy.FULL:
            return f"slot {self.slot} {self.name}: full troops ({self.role.value})"
        split = "/".join(str(value) for value in self.fixed_troops)
        return (
            f"slot {self.slot} {self.name}: fixed split {split}"
            f" ({self.role.value}, exact_required={self.exact_required})"
        )


@dataclass(frozen=True, slots=True)
class TeamPolicyConfig:
    default_skip_if_strategy_missing: bool = True
    notes: str = ""
    teams: tuple[TeamPolicy, ...] = ()

    def find_by_slot(self, slot: int) -> TeamPolicy | None:
        for policy in self.teams:
            if policy.slot == slot:
                return policy
        return None

    def describe_runtime_default(self) -> str:
        return (
            "skip dispatch when no explicit team strategy is configured"
            if self.default_skip_if_strategy_missing
            else "allow default dispatch behavior when no explicit team strategy is configured"
        )


def load_team_policy_config(config: AppConfig) -> TeamPolicyConfig:
    raw_config = config.team_policy
    if not isinstance(raw_config, dict):
        raise ValueError("config/teams.toml must define a top-level mapping")

    raw_policy = raw_config.get("policy", {})
    if raw_policy and not isinstance(raw_policy, dict):
        raise ValueError("[policy] in config/teams.toml must be a table")

    raw_teams = raw_config.get("teams", [])
    if not isinstance(raw_teams, list):
        raise ValueError("config/teams.toml must define [[teams]] entries")

    parsed_teams: list[TeamPolicy] = []
    seen_slots: set[int] = set()
    for raw_team in raw_teams:
        if not isinstance(raw_team, dict):
            raise ValueError("Each [[teams]] entry must be a table")
        team_policy = _parse_team_policy(raw_team)
        if team_policy.slot in seen_slots:
            raise ValueError(f"Duplicate team slot configured: {team_policy.slot}")
        seen_slots.add(team_policy.slot)
        parsed_teams.append(team_policy)

    return TeamPolicyConfig(
        default_skip_if_strategy_missing=bool(raw_policy.get("default_skip_if_strategy_missing", True)),
        notes=str(raw_policy.get("notes", "")),
        teams=tuple(sorted(parsed_teams, key=lambda policy: policy.slot)),
    )


def load_team_policies(config: AppConfig) -> list[TeamPolicy]:
    return list(load_team_policy_config(config).teams)


def _parse_team_policy(raw_team: dict[str, Any]) -> TeamPolicy:
    deployment_policy = DeploymentPolicy(str(raw_team.get("deployment_policy", "full")))
    fixed_values = raw_team.get("fixed_troops", [])
    fixed_troops = tuple(int(value) for value in fixed_values)
    if deployment_policy == DeploymentPolicy.FULL and fixed_troops:
        raise ValueError("full team policies must not define fixed_troops")
    if deployment_policy == DeploymentPolicy.FIXED_SPLIT and not fixed_troops:
        raise ValueError("fixed_split team policies must define fixed_troops")
    if deployment_policy == DeploymentPolicy.FIXED_SPLIT and len(fixed_troops) != 3:
        raise ValueError("fixed_split team policies must define exactly 3 troop values")
    if any(value <= 0 for value in fixed_troops):
        raise ValueError("fixed_troops values must be positive integers")

    slot = int(raw_team["slot"])
    if slot <= 0:
        raise ValueError("team slot must be a positive integer")

    name = str(raw_team["name"]).strip()
    if not name:
        raise ValueError("team name must not be empty")

    return TeamPolicy(
        slot=slot,
        name=name,
        role=TeamRole(str(raw_team.get("role", "main_force"))),
        enabled=bool(raw_team.get("enabled", True)),
        deployment_policy=deployment_policy,
        fixed_troops=fixed_troops,
        exact_required=bool(raw_team.get("exact_required", False)),
        skip_if_insufficient=bool(raw_team.get("skip_if_insufficient", True)),
        notes=str(raw_team.get("notes", "")),
    )
