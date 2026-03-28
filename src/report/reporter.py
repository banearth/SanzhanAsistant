from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.core.runtime import RuntimeContext
from src.state.models import RunSummary


class ReportWriter:
    def __init__(self, ctx: RuntimeContext) -> None:
        self._ctx = ctx

    def write_markdown(self, summary: RunSummary) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = self._ctx.report_dir / f"{timestamp}-{summary.command}.md"
        lines: list[str] = [
            f"# {summary.command}",
            "",
            f"- Started: {summary.started_at.isoformat(timespec='seconds')}",
            f"- Finished: {summary.finished_at.isoformat(timespec='seconds')}",
            "",
            "## Outcomes",
            "",
        ]

        if not summary.outcomes:
            lines.append("- No outcomes recorded.")
        else:
            for outcome in summary.outcomes:
                lines.append(f"- {outcome.name}: {outcome.status.value} - {outcome.detail}")

        lines.extend(["", "## Snapshot", ""])
        if summary.snapshot is None:
            lines.append("- No runtime snapshot.")
        else:
            lines.append(f"- Detected page: {summary.snapshot.detected_page.value}")
            lines.append(f"- Fixture scan count: {summary.snapshot.fixture_scan_count}")
            if summary.snapshot.last_fixture is not None:
                lines.append(f"- Last fixture: {summary.snapshot.last_fixture}")
            if summary.snapshot.notes:
                for note in summary.snapshot.notes:
                    lines.append(f"- Snapshot note: {note}")

        lines.extend(["", "## Notes", ""])
        if not summary.notes:
            lines.append("- No notes.")
        else:
            for note in summary.notes:
                lines.append(f"- {note}")

        output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return output_path
