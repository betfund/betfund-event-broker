"""Module for Intermittent Staging of API Responses."""
import os
from typing import List, Union

from betfund_bet365.response import Bet365Response
from betfund_logger import CloudLogger
from prefect import Task

logger = CloudLogger(
    log_group="betfund-event-broker",
    log_stream="bet365-staging",
    aws_access_key=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_key=os.environ.get("AWS_SECRET_KEY"),
)


class Bet365UpcomingEventsStaging(Task):
    """
    Prepares Bet365 Response Object for Mongo Store.

    Args:
        bet365_response (Bet365Response): API response object

    Returns:
        State: state of prefect `Task`
    """

    def __init__(self):
        """Constructor for Bet365ResponseStaging."""
        super().__init__()

    def run(self, bet365_response: Bet365Response) -> Union[List[dict], None]:
        """
        Ingestion of API Response.

        Args:
            bet365_response (Bet365Response): API response object

        Returns:
            staged_documents (list): list of documents for post
        """
        results = bet365_response.results

        if not results:
            return None

        staged_documents = list(
            map(self.generate_document, results)
        )

        return staged_documents

    @staticmethod
    def generate_document(event: dict) -> dict:
        """
        Create desired document structure for Mongo Collection.

        Args:
            event (dict): Singular raw API Result object

        Returns:
            document (dict): Document conforming payload for MongoDB
        """
        document = {
            "_id": event.id  # creates primary key
        }

        del event["id"]

        event["time"] = int(event["time"])
        document.update({"data": event})

        return document


class Bet365PreMatchOddsStaging(Task):
    """
    Prepares Bet365 PreMatchOdds Response Object for Mongo Store.

    Args:
        bet365_response (Bet365Response): API response object

    Returns:
        State: state of prefect `Task`
    """

    def __init__(self):
        """Constructor for Bet365ResponseStaging."""
        super().__init__()

    def run(self, bet365_response: Bet365Response) -> Union[List[dict], None]:
        """
        Ingestion of API Response.

        Args:
            bet365_response (Bet365Response): API response object

        Returns:
            staged_documents (list): list of documents for post
        """
        results = bet365_response.results

        if not results:
            return None

        staged_documents = list(
            map(self.generate_attributes, results)
        )

        return staged_documents

    @staticmethod
    def generate_attributes(event: dict) -> Union[dict, None]:
        """
        Extract relevant attributes for update to Mongo Collection.

        Args:
            event (dict): Singular raw API Result object

        Returns:
            attributes (dict): Attributes relevant to Mongo upcomingEvents
        """
        if not event.main:
            return {}

        attributes = {
            "_id": event.fi,  # creates primary key
            "odds": event.main.get("sp")
        }

        return attributes
