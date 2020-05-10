"""Unit tests for Helpers tasks"""
from unittest import TestCase

from betfund_event_broker.tasks import Bet365UpcomingEventsStaging
from tests.fixtures import BetfundResponse, MockEvent


class TestBet365UpcomingEventsStaging(TestCase):
    """Unit Test Cases for Bet365UpcomingEventsStaging"""

    def setUp(self) -> None:
        """Instantiate Bet365UpcomingEventsStaging"""
        self.test_task = Bet365UpcomingEventsStaging()

    def test_run(self):
        """Unit test for `Bet365UpcomingEventsStaging.run(...).`"""
        test_response = {
            "results": [
                {
                    "id": "testId",
                    "otherData": "somethingElse",
                    "time": "123"
                },
            ]
        }

        result = self.test_task.run(
            bet365_response=BetfundResponse(test_response)
        )

        assert isinstance(result, list)
        assert result == [
            {
                "_id": "testId",
                "data": {
                    "otherData": "somethingElse",
                    "time": 123
                }
            }
        ]

    def test_generate_document(self):
        """Unit test for `Bet365UpcomingEventsStaging.generate_document(...).`"""
        test_event = {
            "id": "testId",
            "otherData": "somethingElse",
            "time": "123"
        }

        result = self.test_task.generate_document(
            event=MockEvent(test_event)
        )

        assert isinstance(result, dict)
        assert result == {
            "_id": "testId",
            "data": {
                "otherData": "somethingElse",
                "time": 123
            }
        }
