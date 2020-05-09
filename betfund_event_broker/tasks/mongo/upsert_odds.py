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

    def run(self, attributes: dict) -> bool:
        """
        Implements `MongoClient.{database}.{collection}.update_one(...)`.

        Args:
            attributes (list): list of Mongo `documents` to insert

        Returns:
            bool: True if documents were loaded else False
        """
        mongo_client = self._build_client()

        if not attributes:
            return False

        for attribute in attributes:
            pk_id = attribute.get("_id")
            odds = attribute.get("odds", [])

            if not all([pk_id, odds]):
                return False

            mongo_client.betfund.upcomingEvents.update_one(
                {"_id": pk_id},
                {
                    "$set": {
                        "data.odds": odds
                    }
                },
                upsert=True
            )

            mongo_client.close()

            logger.info(
                "UPSERT: ODDS | FI: {}".format(
                    attribute.get("_id")
                )
            )

        return True
