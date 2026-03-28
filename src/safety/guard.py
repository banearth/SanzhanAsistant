from __future__ import annotations

from src.core.runtime import RuntimeContext
from src.state.models import RiskLevel


class SafetyGuard:
    def __init__(self, ctx: RuntimeContext) -> None:
        self._ctx = ctx

    def allows(self, task_name: str, risk_level: RiskLevel) -> bool:
        safety_cfg = self._ctx.config.safety.get("safety", {})
        only_low_risk = safety_cfg.get("allow_only_low_risk_actions", True)
        if not only_low_risk:
            return True
        return risk_level == RiskLevel.LOW
