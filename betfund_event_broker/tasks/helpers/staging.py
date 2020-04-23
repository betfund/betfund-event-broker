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
        document.update({"data": event})

        return document