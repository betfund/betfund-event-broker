"""Unit tests for Bet365 tasks"""
from unittest import TestCase

import mock
from betfund_bet365 import Bet365

from betfund_event_broker.tasks import Bet365PreMatchOdds, Bet365UpcomingEvents
from tests.fixtures import BetfundResponse


class TestBet365UpcomingEvents(TestCase):
    """Unit Test Cases for Bet365UpcomingEvents."""

    def setUp(self) -> None:
        """Instantiate Bet365UpcomingEvents."""
        self.test_task = Bet365UpcomingEvents()
        self.test_task.api_host = "api-host"
        self.test_task.api_key = "you-will-never-guess"

    def test_constructor(self):
        """Unit test for `Bet365UpcomingEvents().__init__(...)`."""
        assert self.test_task.api_host == "api-host"
        assert self.test_task.api_key == "you-will-never-guess"

    @mock.patch.object(Bet365, "upcoming_events")
    def test_run(self, mock_upcoming_events):
        """Unit test for `Bet365UpcomingEvents.run(...)`."""
        mock_upcoming_events.side_effect = [
            BetfundResponse(
                {"results": [{"this": "is"}, {"very": "empty"}]}
            ),
            BetfundResponse(
                {"results": []}
            ),
        ]

        result = self.test_task.run(
            sport="19"
        )

        assert result == [
            {"this": "is"}, {"very": "empty"}
        ]


class TestBet365PreMatchOdds(TestCase):
    """Unit Test Cases for Bet365PreMatchOdds."""

    def setUp(self) -> None:
        """Instantiate PreMatchOdds."""
        self.test_task = Bet365PreMatchOdds()
        self.test_task.api_host = "api-host"
        self.test_task.api_key = "you-will-never-guess"

    def test_constructor(self):
        """Unit test for `Bet365PreMatchOdds().__init__(...)`."""
        assert self.test_task.api_host == "api-host"
        assert self.test_task.api_key == "you-will-never-guess"

    @mock.patch.object(Bet365, "pre_match_odds")
    def test_run(self, mock_pre_match_odds):
        """Unit test for `Bet365PreMatchOdds.run(...)`."""
        mock_pre_match_odds.return_value = None

        result = self.test_task.run(
            document={"_id": "123456"}
        )

        assert result is None
