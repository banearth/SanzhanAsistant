from __future__ import annotations

from pathlib import Path

from src.state.models import PageState, RecognitionResult


KEYWORD_TO_STATE: list[tuple[tuple[str, ...], PageState, str]] = [
    (("home", "city", "main"), PageState.HOME_CITY, "Matched home/city keyword."),
    (("target", "goto", "dispatch"), PageState.ALLIANCE_TARGET_MENU, "Matched alliance-target menu keyword."),
    (("world", "map"), PageState.WORLD_MAP, "Matched world/map keyword."),
    (("alliance", "guild", "union"), PageState.ALLIANCE_TASK_CENTER, "Matched alliance-task keyword."),
    (("task", "quest"), PageState.TASK_CENTER, "Matched task keyword."),
    (("mail", "email"), PageState.MAIL_CENTER, "Matched mail keyword."),
    (("recruit", "conscription", "soldier"), PageState.RECRUIT_PANEL, "Matched recruit keyword."),
    (("battle", "report", "combat"), PageState.BATTLE_REPORT, "Matched battle-report keyword."),
    (("reward", "claim"), PageState.REWARD_POPUP, "Matched reward keyword."),
    (("confirm", "dialog"), PageState.CONFIRM_POPUP, "Matched confirm keyword."),
    (("network", "disconnect", "retry"), PageState.NETWORK_ERROR, "Matched network-error keyword."),
    (("login",), PageState.LOGIN_FLOW, "Matched login keyword."),
]


class KeywordPageStateRecognizer:
    def recognize(self, source: Path) -> RecognitionResult:
        normalized_name = source.stem.lower()
        for keywords, page_state, reason in KEYWORD_TO_STATE:
            if any(keyword in normalized_name for keyword in keywords):
                return RecognitionResult(
                    page_state=page_state,
                    confidence=0.55,
                    reason=reason,
                    source=source,
                )

        return RecognitionResult(
            page_state=PageState.UNKNOWN_STATE,
            confidence=0.1,
            reason="No filename keyword matched. Add better recognizers after collecting real screenshots.",
            source=source,
        )
