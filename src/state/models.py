from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


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
