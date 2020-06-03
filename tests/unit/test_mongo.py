"""Unit tests for Mongo tasks"""
from unittest import TestCase

import mock
from pymongo import MongoClient

from betfund_event_broker.tasks import MongoEventsUpsert
from tests.fixtures import MockMongoConnection


class TestMongoEventsUpsert(TestCase):
    """Unit Test Cases for MongoEventsUpsert."""

    def setUp(self) -> None:
        """Instantiate MongoEventsUpsert."""
        self.test_task = MongoEventsUpsert()
        self.test_task.connect = "server.example.com"

    def test_constructor(self):
        """Unit test for `MongoEventsUpsert().__init__(...)`."""
        assert self.test_task.connect == "server.example.com"

    @mock.patch("pymongo.MongoClient")
    def test_run_empty(self, mock_mongo):
        """Unit test for `MongoEventsUpsert.run(...)` with no documents."""
        mock_mongo.return_value = MockMongoConnection()
        result = self.test_task.run(
            operations=[]
        )

        assert result is False

    @mock.patch("pymongo.MongoClient")
    def test_build_client(self, mock_mongo):
        """Unit test for `MongoEventsUpsert._build_client(...)`."""
        mock_mongo.return_value = MockMongoConnection()
        result = self.test_task._build_client()

        assert isinstance(result, MongoClient)
