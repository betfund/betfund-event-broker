"""Pytest Fixtures and Helpers."""


class MockEvent(dict):
    """Mock Document Object."""
    def __init__(self, data):
        super(MockEvent, self).__init__(data)

    @property
    def id(self):
        """Access for "id"."""
        return self.get("id")


class BetfundResponse(dict):
    """Mock Response Object."""
    def __init__(self, data):
        super(BetfundResponse, self).__init__(data)

    @property
    def results(self):
        """Access for "results"."""
        return list(
            MockEvent(result) for result in self.get("results")
        )


class MockMongoConnection(object):
    """Mock MongoDB Connection."""

    @property
    def betfund(self):
        """Betfund DB Access."""
        return MongoBetfund()


class MongoBetfund(object):
    """Betfund Betfund db Access."""

    @property
    def upcomingEvents(self):  # Intentional camelCase
        """UpcomingEvents Access."""
        return MongoUpcomingEvents()


class MongoUpcomingEvents(object):
    """Betfund UpcomingEvents collection Access."""

    @staticmethod
    def replace_one():
        """Access to `replace_one(...)`."""
        return True
