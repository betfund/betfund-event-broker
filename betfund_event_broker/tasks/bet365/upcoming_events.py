"""Task for handling API Request to UpcomingEvents Endpoint."""
import os
from typing import List, Union

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

    Returns:
        State: state of prefect `Task`
    """

    def run(self, sport: tuple) -> Union[List, None]:
        """
        Executes API Request to `upcoming_events(...)` endpoint.

        Args:
            sport (tuple): Contains sport_id and pretty
            (e.g.)
                ("94", "table-tennis")

        Returns:
            list: Events returned by bet365
        """
        bet365_client = self._build_client()
        sport_id, sport_name = sport

        page = 1
        events = []
        event_results = True
        while event_results:
            response = bet365_client.upcoming_events(
                sport_id=sport_id, page=page
            )
            # Extract `results` attribute
            event_results = response.get("results", [])

            if event_results:
                events.extend(event_results)
                logger.info(
                    "EVENTS: {} | {} RECORDS".format(
                        sport_name.upper(), len(event_results)
                    )
                )

            page += 1

        return events
