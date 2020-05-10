"""Base interface for Prefect Task interaction with MongoDB."""
import os
from abc import abstractmethod

from prefect import Task
from pymongo import MongoClient


class MongoTask(Task):
    """Base class for Prefect Task MonogoDB CRUD."""

    def __init__(self):
        """Constructor for MongoTask"""
        self.connect = os.getenv("MONGO_CONNECTION")
        super().__init__()

    @abstractmethod
    def run(self):
        """
        Method to be implemented by SubClasses.

        `run(...)` will contain business logic for CRUD Action.
        """
        raise NotImplementedError

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
