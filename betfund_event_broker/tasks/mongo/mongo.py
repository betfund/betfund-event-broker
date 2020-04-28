"""MongoDB CRUD Task Modules."""
import os

from betfund_logger import CloudLogger
from prefect import Task
from pymongo import MongoClient

logger = CloudLogger(
    log_group="betfund-event-broker",
    log_stream="mongo-insertion",
    aws_access_key=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_key=os.environ.get("AWS_SECRET_KEY"),
)


class MongoEventsUpsert(Task):
    """
    Inserts documents into Mongo collection.

    Args:
        documents (list): list of documents to be loaded

    Returns:
        State: state of prefect `Task`
    """
    def __init__(self):
        """Constructor for MongoInsertMany."""
        self.connect = os.getenv("MONGO_CONNECTION")
        super().__init__()

    def run(self, documents: list) -> bool:
        """
        Implements `MongoClient.{database}.{collection}.insert_many(...)`.

        Args:
            documents (list): list of Mongo `documents` to insert

        Returns:
            bool: True if documents were loaded else False
        """
        mongo_client = self._build_client()

        if not documents:
            return False

        for document in documents:
            pk_fi = document.get("_id")
            response = mongo_client.betfund.upcomingEvents.replace_one(
                filter={"_id": pk_fi},
                replacement=document,
                upsert=True
            )

            logger.info(
                "FI_ID: {} UPDATED EXISTING: {}".format(
                    pk_fi, response.raw_result.get('updatedExisting')
                )
            )

        return True

    def _build_client(self):
        """
        Build MongoClient.

        Returns:
            mongo_client (MongoClient): MongoDB Client for self.connect
        """
        mongo_client = MongoClient(
            self.connect
        )

        return mongo_client
