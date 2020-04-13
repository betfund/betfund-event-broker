"""TODO"""
import os

from betfund_bet365 import Bet365
from prefect import Task
from prefect.engine.state import State


class Bet365PreMatchOdds(Task):
    """
    Prefect Task for Bet365 API Request.

    Executes GET request to `PreMatch Odds` endpoint

    Args:
        fi (str): Contains unique identifier for an event
            (e.g.)
                "87941408"

    Returns:
        State: state of prefect `Task`
    """

    def __init__(self):
        """Constructor for Bet365UpcomingEvents"""
        self.api_host = os.getenv("BET365_HOST")
        self.api_key = os.getenv("BET365_KEY")
        super().__init__()

    def run(self, fi: str) -> State:
        """
        Executes API Request to `pre_match_odds(...)` endpoint.

    Args:
        fi (str): Contains unique identifier for an event
            (e.g.)
                "87941408"

        Returns:
            tuple: contains API response object and kafka topic
        """
        bet365_client = self._build_client()

        if not fi:
            return None

        response = bet365_client.pre_match_odds(fi=fi)

        print(response)

        return response

    def _build_client(self) -> Bet365:
        """
        Build Bet364 API Wrapper Client.

        NOTE: Clients Must be built  outside of `run(...)` for `Task`
        """
        bet365_client = Bet365(
            api_host=self.api_host, api_key=self.api_key
        )

        return bet365_client
