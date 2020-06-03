"""Unit tests for Helpers tasks"""
from unittest import TestCase

from betfund_event_broker.tasks import Bet365UpcomingEventsStaging


class TestBet365UpcomingEventsStaging(TestCase):
    """Unit Test Cases for Bet365UpcomingEventsStaging"""

    def setUp(self) -> None:
        """Instantiate Bet365UpcomingEventsStaging"""
        self.test_task = Bet365UpcomingEventsStaging()
