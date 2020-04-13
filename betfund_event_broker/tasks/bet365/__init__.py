"""Bet365 namespace."""
from .base import Bet365Task
from .prematch_odds import Bet365PreMatchOdds
from .upcoming_events import Bet365UpcomingEvents

__all__ = [
    "Bet365Task",
    "Bet365PreMatchOdds",
    "Bet365UpcomingEvents"
]
