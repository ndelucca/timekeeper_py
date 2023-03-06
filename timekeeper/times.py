"""Time management utils"""
from datetime import datetime
from typing import List

ROUND_INTERVAL = 5


def round_minutes(minutes: int, interval: int = ROUND_INTERVAL) -> int:
    """Rounds received minutos to an interval fraction"""
    return interval * int(minutes / interval)


def now_rounded(interval: int = ROUND_INTERVAL) -> datetime:
    """Returns a rounded minutes now datetime"""
    now = datetime.now()
    current_minutes = now.minute
    return now.replace(
        minute=round_minutes(current_minutes, interval), second=0, microsecond=0
    )
