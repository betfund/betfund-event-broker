"""MongoDB Update Task Module."""
import os

from betfund_logger import CloudLogger

from betfund_event_broker.tasks.mongo import MongoTask

logger = CloudLogger(
    log_group="betfund-event-broker",
    log_stream="mongo-update-odds",
    aws_access_key=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_key=os.environ.get("AWS_SECRET_KEY"),
)


class MongoOddsUpsert(MongoTask):
    """
    Inserts documents into Mongo collection.

    Args:
        documents (list): list of documents to be loaded

    Returns:
        State: state of prefect `Task`
    """
    def __init__(self):
        """Constructor for MongoOddsUpsert."""
        self.connect = os.getenv("MONGO_CONNECTION")
        super().__init__()

    def run(self, documents: list) -> bool:
        """
        Implements `MongoClient.{database}.{collection}.update_one(...)`.

        Args:
            documents (list): list of Mongo `documents` to insert

        Returns:
            bool: True if documents were loaded else False
        """
        mongo_client = self._build_client()

        if not documents:
            return False

        for document in documents:
            if not document:
                return False

            pk_id = document.get("_id")
            odds = document.get("odds") or None

            mongo_client.betfund.upcomingEvents.update_one(
                filter={"_id": pk_id},
                update={
                    "$set": {
                        "data.odds": odds
                    }
                },
                upsert=True
            )

            logger.info(
                "UPSERT: ODDS | FI: {}".format(
                    document.get("_id")
                )
            )

        return True
