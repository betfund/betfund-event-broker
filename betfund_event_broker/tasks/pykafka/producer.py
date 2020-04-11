"""Kafka Publish Modules."""
import json
import os

from kafka import KafkaProducer
from prefect import Task


class EventProducer(Task):
    """
    Event Producer Object.
    EventProducer handles produces events via `.send(...)` in a Kafka topic
    Args:
        payload (dict): Bet365 API Response
        endpoint (str): Endpoint name to dictate topic
    Returns:
        response (FutureRecordMetadata): resolves to RecordMetadata
    """

    def __init__(self):
        """Constructor for EventProducer."""
        self.server = os.getenv("KAFKA_BOOTSTRAP_SERVER")  # temporary
        super().__init__()

    def run(self, asset: tuple):
        """
        Implements `KafkaProducer.send(...)`.
        Args:
            record (dict): Record produced by `RundownTransformer`
        Returns:
            response (FutureRecordMetadata): resolves to RecordMetadata
        Raises:
            MalformedPayloadError: if `record` is not literal `dict`
        """
        producer = self._build_producer()

        payload = asset[0]
        topic = asset[1]

        response = producer.send(
            topic=topic, value=payload
        )

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
