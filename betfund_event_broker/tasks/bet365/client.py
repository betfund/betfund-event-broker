"""TODO"""
import os

from betfund_bet365 import Bet365
from prefect import Task
from prefect.engine.state import State


class Bet365UpcomingEvents(Task):
    """
    Prefect Task for Bet365 API Request.

    Executes GET request to `Upcoming Events` endpoint

    Args:
        sport (tuple): Contains sport_id and pretty
            (e.g.)
                ("94", "table-tennis")

    Returns:
        State: state of prefect `Task`
    """

    topic = "upcomingEvents"

    def __init__(self):
        """Constructor for Bet365UpcomingEvents"""
        self.api_host = os.getenv("BET365_HOST")
        self.api_key = os.getenv("BET365_KEY")
        super().__init__()

    def run(self, sport: tuple) -> State:
        """
        Executes API Request to `upcoming_events(...)` endpoint.

        Args:
            sport (tuple): Contains sport_id and pretty
            (e.g.)
                ("94", "table-tennis")

        Returns:
            tuple: contains API response object and kafka topic
        """
        bet365_client = self._build_client()

        response = bet365_client.upcoming_events(sport_id=sport[0])

        return response, self.topic

    def _build_client(self) -> Bet365:
        """
        Build Bet364 API Wrapper Client.

        NOTE: Clients Must be built  outside of `run(...)` for `Task`
        """
        bet365_client = Bet365(
            api_host=self.api_host, api_key=self.api_key
        )

        return bet365_client
