from __future__ import annotations

from pathlib import Path
from typing import Protocol

from src.state.models import RecognitionResult


class PageRecognizer(Protocol):
    def recognize(self, source: Path) -> RecognitionResult:
        ...
