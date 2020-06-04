"""Module for Intermittent Staging of API Responses."""
import os
from typing import List, Union

from betfund_bet365.response import Bet365Response
from betfund_logger import CloudLogger
from prefect import Task
from pymongo import ReplaceOne, UpdateOne

logger = CloudLogger(
    log_group="betfund-event-broker",
    log_stream="bet365-staging",
    aws_access_key=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_key=os.environ.get("AWS_SECRET_KEY"),
)


class Bet365UpcomingEventsStaging(Task):
    """
    Prepares Bet365 Response Object for Mongo Store.

    Returns:
        State: state of prefect `Task`
    """

    def __init__(self):
        """Constructor for Bet365ResponseStaging."""
        super().__init__()

    def run(self, results: list) -> Union[List[ReplaceOne], None]:
        """
        Ingestion of API Response.

        Args:
            results (list): List of `results` objects

        Returns:
            staged_document (ReplaceOne): Mongo Operator for upsert
        """
        if not results:
            return None

        staged_document = list(
            map(self.generate_operator, results)
        )

        return staged_document

    @staticmethod
    def generate_operator(event: dict) -> Union[ReplaceOne, None]:
        """
        Create desired document structure for Mongo Collection.

        Args:
            event (dict): Singular raw API Result object

        Returns:
            operator (ReplaceOne): Mongo Operator for upsert
        """
        if not event.get("id"):
            return None

        document = {
            "_id": event.get("id")  # creates primary key
        }

        del event["id"]
        event["time"] = int(event["time"])
        document.update({"data": event})

        operator = ReplaceOne(
            filter={"_id": document.get("_id")},
            replacement=document,
            upsert=True
        )

        return operator


class Bet365PreMatchOddsStaging(Task):
    """
    Prepares Bet365 PreMatchOdds Response Object for Mongo Store.

    Returns:
        State: state of prefect `Task`
    """

    def __init__(self):
        """Constructor for Bet365ResponseStaging."""
        super().__init__()

    def run(
        self, bet365_response: Bet365Response
    ) -> Union[List[UpdateOne], None]:
        """
        Ingestion of API Response.

        Args:
            bet365_response (Bet365Response): API response object

        Returns:
            staged_document (UpdateOne): Monogo Operator for upsert
        """
        results = bet365_response.results

        if not results:
            return None

        staged_document = list(
            map(self.generate_operator, results)
        )

        return staged_document

    @staticmethod
    def generate_operator(event: dict) -> Union[UpdateOne, None]:
        """
        Extract relevant attributes for update to Mongo Collection.

        Args:
            event (dict): Singular raw API Result object

        Returns:
            operator (UpdateOne): Monogo Operator for upsert
        """
        if not event.main:
            return None

        odds = event.main.get("sp")

        operator = UpdateOne(
            filter={"_id": event.fi},
            update={
                "$set": {
                    "data.odds": odds
                }
            },
            upsert=True
        )

        return operator
