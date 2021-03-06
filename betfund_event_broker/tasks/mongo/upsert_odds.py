"""MongoDB Update Task Module."""
import itertools
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
        operations (list): list of Mongo Operations to be loaded

    Returns:
        State: state of prefect `Task`
    """
    def __init__(self):
        """Constructor for MongoOddsUpsert."""
        self.connect = os.getenv("MONGO_CONNECTION")
        super().__init__()

    def run(self, operations: list) -> bool:
        """
        Implements `MongoClient.{database}.{collection}.bulk_write(...)`.

        Args:
            operations (list): list of Mongo `documents` to upsert

        Returns:
            bool: True if documents were loaded else False
        """
        mongo_client = self._build_client()

        if not operations:
            return False

        operation_set = itertools.chain.from_iterable(operations)
        valid_operations = [op for op in operation_set if op]

        mongo_client.betfund.upcomingEvents.bulk_write(
            valid_operations,
            ordered=True
        )

        mongo_client.close()
        logger.info(
            "BULK UPSERT: PRE-MATCH ODDS | EVENTS: {}".format(
                len(valid_operations)
            )
        )

        return True
