from __future__ import annotations

import argparse
from pathlib import Path

from src.agent.device import DeviceAdapter
from src.core.config import load_app_config
from src.core.runtime import RuntimeContext
from src.pipelines.daily_runner import DailyRunner
from src.report.reporter import ReportWriter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sanzhan Assistant scaffold entrypoint.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("check-env", help="Validate basic project layout and config files.")
    subparsers.add_parser("run-daily", help="Run the scaffold daily flow and write a report.")
    subparsers.add_parser("debug-capture", help="Create a placeholder debug report for capture work.")
    subparsers.add_parser("inspect-fixtures", help="Inspect screenshot fixture filenames and guess page states.")
    subparsers.add_parser("print-config", help="Print resolved config paths.")
    return parser


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def make_context() -> RuntimeContext:
    root = project_root()
    config = load_app_config(root / "config")
    return RuntimeContext(root_dir=root, config=config)


def run_check_env(ctx: RuntimeContext) -> int:
    device_health = DeviceAdapter(ctx).health_check()
    required_paths = [
        ctx.root_dir / "interface.json",
        ctx.root_dir / "config" / "default.toml",
        ctx.root_dir / "config" / "tasks.toml",
        ctx.root_dir / "config" / "safety.toml",
        ctx.root_dir / "resource" / "pipeline",
        ctx.root_dir / "src",
    ]
    missing = [str(path) for path in required_paths if not path.exists()]
    if missing:
        print("Environment check failed. Missing paths:")
        for item in missing:
            print(f"- {item}")
        return 1

    print("Environment check passed.")
    print(f"Project root: {ctx.root_dir}")
    print(f"Controller type: {device_health.controller_type}")
    print(f"Configured serial: {device_health.serial}")
    print(f"Controller ready: {device_health.is_ready}")
    print(f"Daily reports: {ctx.config.runtime['report_dir']}")
    print(f"Screenshots: {ctx.config.runtime['screenshot_dir']}")
    print(f"Fixture dir: {ctx.fixture_dir}")
    print(f"Note: {device_health.note}")
    return 0


def run_daily(ctx: RuntimeContext) -> int:
    runner = DailyRunner(ctx)
    summary = runner.run()
    report_path = ReportWriter(ctx).write_markdown(summary)
    print(f"Daily scaffold run finished. Report written to: {report_path}")
    return 0


def run_debug_capture(ctx: RuntimeContext) -> int:
    summary = DailyRunner(ctx).debug_capture()
    report_path = ReportWriter(ctx).write_markdown(summary)
    print(f"Debug scaffold report written to: {report_path}")
    return 0


def run_inspect_fixtures(ctx: RuntimeContext) -> int:
    summary = DailyRunner(ctx).inspect_fixtures()
    report_path = ReportWriter(ctx).write_markdown(summary)
    print(f"Fixture inspection report written to: {report_path}")
    return 0


def run_print_config(ctx: RuntimeContext) -> int:
    print(f"Root: {ctx.root_dir}")
    print(f"Default config: {ctx.root_dir / 'config' / 'default.toml'}")
    print(f"Task config: {ctx.root_dir / 'config' / 'tasks.toml'}")
    print(f"Safety config: {ctx.root_dir / 'config' / 'safety.toml'}")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    ctx = make_context()

    if args.command == "check-env":
        return run_check_env(ctx)
    if args.command == "run-daily":
        return run_daily(ctx)
    if args.command == "debug-capture":
        return run_debug_capture(ctx)
    if args.command == "inspect-fixtures":
        return run_inspect_fixtures(ctx)
    if args.command == "print-config":
        return run_print_config(ctx)

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
