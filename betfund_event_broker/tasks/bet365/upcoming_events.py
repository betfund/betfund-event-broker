"""TODO"""
from operator import itemgetter

from typing import Union

from betfund_bet365.response import Bet365Response
from betfund_event_broker.tasks.bet365 import Bet365Task


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

    def run(self, sport: tuple) -> Union[None, Bet365Response]:
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

        response = bet365_client.upcoming_events(sport_id=sport[0])

        if not response.events:
            return None

        fi_list = list(map(itemgetter('id'), response.events))

        return fi_list
