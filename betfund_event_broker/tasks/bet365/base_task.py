"""TODO"""
import os

from abc import abstractmethod

from betfund_bet365 import Bet365
from prefect import Task


class Bet365Task(Task):
    """Base class for Prefect Task Bet365 API Requests."""

    def __init__(self):
        """Constructor for Bet365Task"""
        self.api_host = os.getenv("BET365_HOST")
        self.api_key = os.getenv("BET365_KEY")
        super().__init__()

    @abstractmethod
    def run(self):
        """
        Method to be implemented by Base Classes.

        `run(...)` will contain business logic for API Request.
        """
        raise NotImplementedError

    def _build_client(self) -> Bet365:
        """
        Build Bet365 API Wrapper Client.

        NOTE: Clients Must be built outside of `run(...)` for `Task`
        """
        bet365_client = Bet365(api_host=self.api_host, api_key=self.api_key)

        return bet365_client
