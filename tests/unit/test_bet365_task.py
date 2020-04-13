"""Unit tests for Bet365 tasks"""

from unittest import TestCase

from betfund_event_broker.tasks.bet365 import Bet365UpcomingEvents


class TestBet365UpcomingEvents(TestCase):
    """Unit Test Cases for Bet365UpcomingEvents"""

    def setUp(self) -> None:
        """Instantiate Bet365UpcomingEvents"""
        self.test_client = Bet365UpcomingEvents()
        self.test_client.api_host = "api-host"
        self.test_client.api_key = "you-will-never-guess"

    def test_constructor(self):
        """Unit test for `Bet365UpcomingEvents().__init__(...)`"""
        assert self.test_client.api_host == "api-host"
        assert self.test_client.api_key == "you-will-never-guess"
