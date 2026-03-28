from __future__ import annotations

from dataclasses import dataclass

from src.state.models import PageState, RiskLevel


@dataclass(frozen=True, slots=True)
class DailyTaskDefinition:
    name: str
    label: str
    risk_level: RiskLevel
    preferred_page: PageState
    detail: str


TASK_REGISTRY: dict[str, DailyTaskDefinition] = {
    "collect_mail": DailyTaskDefinition(
        name="collect_mail",
        label="Collect Mail",
        risk_level=RiskLevel.LOW,
        preferred_page=PageState.MAIL_CENTER,
        detail="Collect rewards from the in-game mail center.",
    ),
    "collect_tasks": DailyTaskDefinition(
        name="collect_tasks",
        label="Collect Tasks",
        risk_level=RiskLevel.LOW,
        preferred_page=PageState.TASK_CENTER,
        detail="Claim completed daily or growth task rewards.",
    ),
    "collect_general_rewards": DailyTaskDefinition(
        name="collect_general_rewards",
        label="Collect General Rewards",
        risk_level=RiskLevel.LOW,
        preferred_page=PageState.HOME_CITY,
        detail="Collect general low-risk reward popups or entry rewards.",
    ),
    "recruit_safe_mode": DailyTaskDefinition(
        name="recruit_safe_mode",
        label="Recruit Safe Mode",
        risk_level=RiskLevel.LOW,
        preferred_page=PageState.RECRUIT_PANEL,
        detail="Top up a safe baseline of recruitment or conscription actions.",
    ),
    "battle_scout_only": DailyTaskDefinition(
        name="battle_scout_only",
        label="Battle Scout Only",
        risk_level=RiskLevel.MEDIUM,
        preferred_page=PageState.WORLD_MAP,
        detail="Reserve slot for future battle-only reconnaissance suggestions.",
    ),
}
