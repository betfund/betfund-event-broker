"""TODO"""
from typing import Union

from betfund_bet365.response import Bet365Response
from betfund_event_broker.tasks.bet365 import Bet365Task


class Bet365PreMatchOdds(Bet365Task):
    """
    Executes GET request to `PreMatch Odds` endpoint.

    Args:
        fi (str): Contains unique identifier for an event
            (e.g.)
                "87941408"

    Returns:
        State: state of prefect `Task`
    """
    topic = "preMatchOdds"

    def run(self, fi: str) -> Union[None, Bet365Response]:
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
            return None, self.topic  # this needs to be amended

        response = bet365_client.pre_match_odds(fi=fi)

        return response, self.topic
