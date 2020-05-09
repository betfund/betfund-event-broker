"""Task for handling API Request to PreMatch Odds Endpoint."""
import json
import os
from typing import Union

from betfund_bet365.response import Bet365Response
from betfund_logger import CloudLogger

from betfund_event_broker.tasks.bet365 import Bet365Task

logger = CloudLogger(
    log_group="betfund-event-broker",
    log_stream="bet365-pre-match-odds",
    aws_access_key=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_key=os.environ.get("AWS_SECRET_KEY"),
)


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

    def run(self, documents: dict) -> Union[Bet365Response, None]:
        """
        Executes API Request to `pre_match_odds(...)` endpoint.

        Args:
            document (dict): MongoDB document

        Returns:
            tuple: contains API response object and kafka topic
        """
        bet365_client = self._build_client()

        fi = documents.get("_id")

        if not fi:
            return None

        response = bet365_client.pre_match_odds(fi=fi)

        logger.debug(
            f"<{self.__class__.__name__}> RESPONSE: {json.dumps(response)}"
        )

        return response
