"""MongoDB CRUD Modules."""
import os
from typing import Union

from betfund_logger import CloudLogger
from prefect import Task
from pymongo import MongoClient
from pymongo.results import InsertManyResult

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

    def run(self, documents: list) -> Union[InsertManyResult, None]:
        """
        Implements `MongoClient.{database}.{collection}.insert_many(...)`.

        Args:
            events (list): list of Mongo `documents` to insert

        Returns:
            response (FutureRecordMetadata): resolves to RecordMetadata
        """
        mongo_client = self._build_client()
        upcoming_events_collection = mongo_client.betfund.upcomingEvents

        if not documents:
            return None

        for document in documents:
            pk_fi = document.get("_id")
            response = upcoming_events_collection.replace_one(
                filter={"_id": pk_fi},
                replacement=document,
                upsert=True
            )

            logger.info(
                "FI_ID: {} UPDATED EXISTING: {}".format(
                    pk_fi, response.raw_result.get('updatedExisting')
                )
            )

        return "Finished"

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
