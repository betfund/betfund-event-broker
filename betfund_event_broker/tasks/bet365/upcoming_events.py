"""Task for handling API Request to UpcomingEvents Endpoint."""
import os
from typing import Union

from betfund_bet365.response import Bet365Response
from betfund_logger import CloudLogger
from betfund_event_broker.tasks.bet365 import Bet365Task

logger = CloudLogger(
    log_group="betfund-event-broker",
    log_stream="bet365-upcoming-events",
    aws_access_key=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_key=os.environ.get("AWS_SECRET_KEY"),
)


class Bet365UpcomingEvents(Bet365Task):
    """
    Executes GET request to `Upcoming Events` endpoint.

    Args:
        sport (tuple): Contains sport_id and pretty
            (e.g.)
                ("94", "table-tennis")

    Returns:
        State: state of prefect `Task`
    """

    def run(self, sport: tuple) -> Union[Bet365Response, None]:
        """
        Executes API Request to `upcoming_events(...)` endpoint.

        Args:
            sport (tuple): Contains sport_id and pretty
            (e.g.)
                ("94", "table-tennis")

        Returns:
            Bet365Response: response object from betfund-bet365
        """
        bet365_client = self._build_client()

        sport_id = sport[0]
        sport_name = sport[1]

        response = bet365_client.upcoming_events(sport_id=sport_id)

        logger.info(
            f"<{sport_name.upper()}> RETURNED {len(response)} RECORDS"
        )

        return response
