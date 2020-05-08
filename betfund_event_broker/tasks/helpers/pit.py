"""Module for Generating Point In Time timestamp."""
import time

from prefect import Task


class PointInTime(Task):
    """
    Generate PointInTime epoch timestamp.

    Returns:
        State: state of prefect `Task`
    """

    def __init__(self):
        """Constructor for Bet365ResponseStaging."""
        super().__init__()

    def run(self) -> int:
        """
        Execute PointInTime Task.

        Returns:
            timestamp (int): Current time epoch timestamp
        """
        timestamp = round(time.time())

        return timestamp
