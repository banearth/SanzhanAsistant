from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


class TaskStatus(str, Enum):
    SUCCESS = "SUCCESS"
    SKIPPED = "SKIPPED"
    FAILED_RETRYABLE = "FAILED_RETRYABLE"
    FAILED_NON_RETRYABLE = "FAILED_NON_RETRYABLE"
    STOPPED_BY_SAFETY = "STOPPED_BY_SAFETY"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PageState(str, Enum):
    APP_LAUNCHING = "APP_LAUNCHING"
    LOGIN_FLOW = "LOGIN_FLOW"
    HOME_CITY = "HOME_CITY"
    WORLD_MAP = "WORLD_MAP"
    TASK_CENTER = "TASK_CENTER"
    ALLIANCE_TASK_CENTER = "ALLIANCE_TASK_CENTER"
    MAIL_CENTER = "MAIL_CENTER"
    RECRUIT_PANEL = "RECRUIT_PANEL"
    BATTLE_REPORT = "BATTLE_REPORT"
    REWARD_POPUP = "REWARD_POPUP"
    CONFIRM_POPUP = "CONFIRM_POPUP"
    NETWORK_ERROR = "NETWORK_ERROR"
    UNKNOWN_STATE = "UNKNOWN_STATE"


@dataclass(slots=True)
class RecognitionResult:
    page_state: PageState
    confidence: float
    reason: str
    source: Path | None = None


@dataclass(slots=True)
class RuntimeSnapshot:
    detected_page: PageState
    fixture_scan_count: int = 0
    last_fixture: Path | None = None
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class TaskOutcome:
    name: str
    status: TaskStatus
    detail: str


@dataclass(slots=True)
class RunSummary:
    command: str
    started_at: datetime
    finished_at: datetime
    outcomes: list[TaskOutcome] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    snapshot: RuntimeSnapshot | None = None
