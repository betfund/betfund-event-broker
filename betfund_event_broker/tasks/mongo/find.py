"""MongoDB Find Task Module."""
import os

from betfund_logger import CloudLogger

from betfund_event_broker.tasks.mongo import MongoTask

logger = CloudLogger(
    log_group="betfund-event-broker",
    log_stream="mongo-find-events",
    aws_access_key=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_key=os.environ.get("AWS_SECRET_KEY"),
)


class MongoFindEvents(MongoTask):
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

    def run(self, epoch: int) -> bool:
        """
        Implements `MongoClient.{database}.{collection}.insert_many(...)`.

        Args:
            epoch (int): Epoch timestamp for run initiation

        Returns:
            documents (list): Documents fetched from MongoDB
        """
        mongo_client = self._build_client()

        if not epoch:
            return False

        cursor = mongo_client.betfund.upcomingEvents.find(
            filter={
                "data.time": {
                    "$gt": epoch
                }
            }
        )

        documents = []
        for event in cursor:
            documents.append(event)

        logger.info(
            "FOUND {} RECORDS: AFTER {}".format(
                len(documents), epoch
            )
        )

        return documents
