from __future__ import annotations

from datetime import datetime

from src.core.runtime import RuntimeContext
from src.safety.guard import SafetyGuard
from src.state.models import RiskLevel, RunSummary, TaskOutcome, TaskStatus


TASK_TO_RISK = {
    "collect_mail": RiskLevel.LOW,
    "collect_tasks": RiskLevel.LOW,
    "collect_general_rewards": RiskLevel.LOW,
    "recruit_safe_mode": RiskLevel.LOW,
    "battle_scout_only": RiskLevel.MEDIUM,
}


class DailyRunner:
    def __init__(self, ctx: RuntimeContext) -> None:
        self._ctx = ctx
        self._guard = SafetyGuard(ctx)

    def run(self) -> RunSummary:
        started_at = datetime.now()
        outcomes: list[TaskOutcome] = []
        notes = [
            "This is a scaffold run. MaaFramework controller integration is not wired yet.",
            "Use this report shape as the baseline for future real task execution.",
        ]

        configured_tasks = self._ctx.config.tasks.get("tasks", {})
        ordered_names = self._ctx.config.tasks.get("ordering", [])

        for task_name in ordered_names:
            enabled = bool(configured_tasks.get(task_name, False))
            risk_level = TASK_TO_RISK.get(task_name, RiskLevel.LOW)

            if not enabled:
                outcomes.append(
                    TaskOutcome(
                        name=task_name,
                        status=TaskStatus.SKIPPED,
                        detail="Disabled in config/tasks.yaml",
                    )
                )
                continue

            if not self._guard.allows(task_name, risk_level):
                outcomes.append(
                    TaskOutcome(
                        name=task_name,
                        status=TaskStatus.STOPPED_BY_SAFETY,
                        detail=f"Blocked by safety policy for risk level {risk_level.value}",
                    )
                )
                continue

            outcomes.append(
                TaskOutcome(
                    name=task_name,
                    status=TaskStatus.SUCCESS,
                    detail="Accepted by scaffold pipeline. Replace with real recognizer/action flow next.",
                )
            )

        return RunSummary(
            command="run-daily",
            started_at=started_at,
            finished_at=datetime.now(),
            outcomes=outcomes,
            notes=notes,
        )

    def debug_capture(self) -> RunSummary:
        started_at = datetime.now()
        return RunSummary(
            command="debug-capture",
            started_at=started_at,
            finished_at=datetime.now(),
            outcomes=[
                TaskOutcome(
                    name="debug_capture",
                    status=TaskStatus.SUCCESS,
                    detail="Scaffold report generated. Next step is wiring actual screenshot capture and sample storage.",
                )
            ],
            notes=[
                "Collect screenshots for HOME_CITY, WORLD_MAP, TASK_CENTER, MAIL_CENTER, RECRUIT_PANEL.",
                "Add popup samples for rewards, confirms, network errors, and unknown states.",
            ],
        )
