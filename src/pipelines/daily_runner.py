from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.core.runtime import RuntimeContext
from src.planner.team_policy import load_team_policy_config
from src.pipelines.task_registry import TASK_REGISTRY
from src.recognizers.page_state import KeywordPageStateRecognizer
from src.safety.guard import SafetyGuard
from src.state.models import PageState, RunSummary, RuntimeSnapshot, TaskOutcome, TaskStatus


class DailyRunner:
    def __init__(self, ctx: RuntimeContext) -> None:
        self._ctx = ctx
        self._guard = SafetyGuard(ctx)
        self._page_recognizer = KeywordPageStateRecognizer()

    def run(self) -> RunSummary:
        started_at = datetime.now()
        outcomes: list[TaskOutcome] = []
        snapshot = self._build_snapshot()
        notes = [
            "This is a scaffold run. MaaFramework controller integration is not wired yet.",
            "Use this report shape as the baseline for future real task execution.",
            "For SanZhan, alliance tasks are modeled as the meaningful battle-facing daily loop rather than ordinary reward claims.",
        ]
        notes.extend(self._team_policy_notes())
        notes.extend(snapshot.notes)

        configured_tasks = self._ctx.config.tasks.get("tasks", {})
        workflow_cfg = self._ctx.config.tasks.get("workflow", {})
        ordered_names = workflow_cfg.get("ordering", [])

        for task_name in ordered_names:
            enabled = bool(configured_tasks.get(task_name, False))
            task_definition = TASK_REGISTRY.get(task_name)
            if task_definition is None:
                outcomes.append(
                    TaskOutcome(
                        name=task_name,
                        status=TaskStatus.FAILED_NON_RETRYABLE,
                        detail="Task is enabled in config but missing from TASK_REGISTRY.",
                    )
                )
                continue

            if not enabled:
                outcomes.append(
                    TaskOutcome(
                        name=task_name,
                        status=TaskStatus.SKIPPED,
                        detail="Disabled in config/tasks.toml",
                    )
                )
                continue

            if not self._guard.allows(task_name, task_definition.risk_level):
                outcomes.append(
                    TaskOutcome(
                        name=task_name,
                        status=TaskStatus.STOPPED_BY_SAFETY,
                        detail=f"Blocked by safety policy for risk level {task_definition.risk_level.value}",
                    )
                )
                continue

            outcomes.append(
                TaskOutcome(
                    name=task_name,
                    status=TaskStatus.SUCCESS,
                    detail=(
                        f"Accepted by scaffold pipeline. Preferred page: {task_definition.preferred_page.value}. "
                        f"Planned action: {task_definition.detail}"
                    ),
                )
            )

        return RunSummary(
            command="run-daily",
            started_at=started_at,
            finished_at=datetime.now(),
            outcomes=outcomes,
            notes=notes,
            snapshot=snapshot,
        )

    def debug_capture(self) -> RunSummary:
        started_at = datetime.now()
        snapshot = self._build_snapshot()
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
            snapshot=snapshot,
        )

    def inspect_fixtures(self) -> RunSummary:
        started_at = datetime.now()
        fixture_files = self._list_fixture_files()
        outcomes: list[TaskOutcome] = []

        for fixture in fixture_files:
            result = self._page_recognizer.recognize(fixture)
            outcomes.append(
                TaskOutcome(
                    name=fixture.name,
                    status=TaskStatus.SUCCESS,
                    detail=f"{result.page_state.value} ({result.reason})",
                )
            )

        notes = [
            "Fixture inspection uses filename keywords only for now.",
            "Once real screenshots exist, replace this with template/OCR-based recognition.",
        ]
        if not fixture_files:
            notes.append("No fixture images were found under tests/fixtures.")

        snapshot = self._build_snapshot()
        return RunSummary(
            command="inspect-fixtures",
            started_at=started_at,
            finished_at=datetime.now(),
            outcomes=outcomes,
            notes=notes,
            snapshot=snapshot,
        )

    def _build_snapshot(self) -> RuntimeSnapshot:
        fixture_files = self._list_fixture_files()
        if not fixture_files:
            return RuntimeSnapshot(
                detected_page=PageState.UNKNOWN_STATE,
                fixture_scan_count=0,
                notes=["No screenshot fixtures collected yet."],
            )

        latest_fixture = fixture_files[-1]
        latest_result = self._page_recognizer.recognize(latest_fixture)
        return RuntimeSnapshot(
            detected_page=latest_result.page_state,
            fixture_scan_count=len(fixture_files),
            last_fixture=latest_fixture,
            notes=[
                f"Latest fixture guess: {latest_result.page_state.value}",
                f"Latest fixture file: {latest_fixture.name}",
            ],
        )

    def _list_fixture_files(self) -> list[Path]:
        fixture_dir = self._ctx.fixture_dir
        if not fixture_dir.exists():
            return []
        allowed_suffixes = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}
        return sorted(
            path for path in fixture_dir.rglob("*") if path.is_file() and path.suffix.lower() in allowed_suffixes
        )

    def _team_policy_notes(self) -> list[str]:
        team_config = load_team_policy_config(self._ctx.config)
        notes = [f"Team policy default: {team_config.describe_runtime_default()}"]
        if team_config.notes:
            notes.append(f"Team policy notes: {team_config.notes}")
        for policy in team_config.teams:
            notes.append(policy.describe())
        return notes
