"""Kafka Publish Modules."""
import json
import os

from betfund_logger import CloudLogger
from kafka import KafkaProducer
from prefect import Task

logger = CloudLogger(
    log_group="betfund-event-broker",
    log_stream="kafka-producer",
    aws_access_key=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_key=os.environ.get("AWS_SECRET_KEY"),
)


class KafkaMessageProducer(Task):
    """
    KafkaMessageProducer Task.

    KafkaMessageProducer produces events via `.send(...)` in a Kafka topic
    Args:
        asset (tuple): tuple that contains (payload, endpiont)
            payload (dict): Bet365 API Response
            endpoint (str): Endpoint name to dictate topic
    Returns:
        response (FutureRecordMetadata): resolves to RecordMetadata
    """

    def __init__(self):
        """Constructor for EventProducer."""
        self.server = os.getenv("KAFKA_BOOTSTRAP_SERVER")
        super().__init__()

    def run(self, asset: tuple):
        """
        Implements `KafkaProducer.send(...)`.

        Args:
            asset (tuple): tuple that contains (payload, endpoint)
                payload (dict): Bet365 API Response
                endpoint (str): Endpoint name to dictate topic
        Returns:
            response (FutureRecordMetadata): resolves to RecordMetadata
        """
        producer = self._build_producer()

        # Destructure tuple
        payload = asset[0]
        topic = asset[1]

        if not payload:
            return None

        response = producer.send(topic=topic, value=payload)

        logger.info(f"TOPIC: {topic} RESPONSE: {response}")

        return response

    def _build_producer(self):
        """
        Build KafkaProducer Client.

        Returns:
            producer (KafkaProducer): Kafka Producer for self.server
        """
        producer = KafkaProducer(
            bootstrap_servers=self.server,
            value_serializer=(
                lambda mes: json.dumps(mes).encode("utf-8")
            ),
        )

        return producer
