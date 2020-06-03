"""MongoDB Upsert Task Module."""
import os

from betfund_logger import CloudLogger

from betfund_event_broker.tasks.mongo import MongoTask

logger = CloudLogger(
    log_group="betfund-event-broker",
    log_stream="mongo-upsert-event",
    aws_access_key=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_key=os.environ.get("AWS_SECRET_KEY"),
)


class MongoEventsUpsert(MongoTask):
    """
    Inserts documents into Mongo collection.

    Args:
        operations (list): list of Mongo Operations to be loaded

    Returns:
        State: state of prefect `Task`
    """
    def __init__(self):
        """Constructor for MongoInsertMany."""
        self.connect = os.getenv("MONGO_CONNECTION")
        super().__init__()

    def run(self, operations: list) -> bool:
        """
        Implements `MongoClient.{database}.{collection}.replace_one(...)`.

        Args:
            operations (list): list of Mongo `documents` to insert

        Returns:
            bool: True if documents were loaded else False
        """
        mongo_client = self._build_client()

        if not operations:
            return False

        mongo_client.betfund.upcomingEvents.bulk_write(
            operations,
            ordered=True
        )

        mongo_client.close()
        logger.info(
            "BULK UPSERT: UPCOMING EVENTS | DOCUMENTS: {}".format(
                len(operations)
            )
        )

        return True
