"""Unit tests for Base flow"""
from unittest import TestCase

import mock
import pytest
from prefect import Flow

from betfund_event_broker.flows import EventBrokerFlow, UpcomingEventsFlow


class TestEventBrokerFlow(TestCase, EventBrokerFlow):
    """Unit Test Cases for EventBrokerFlow."""

    @mock.patch.multiple(EventBrokerFlow, __abstractmethods__=set())
    def setUp(self) -> None:
        """Instantiate EventBrokerFlow."""
        self.instance = EventBrokerFlow()
        self.distributed = False
        self.scheduled = False

    def test_constructor(self):
        """Unit test for `EventBrokerFlow().__init__(...)`."""
        assert self.distributed is False
        assert self.scheduled is False

    def build(self, *args, **kwargs):
        """Implement `build(...)`."""
        pass

    def test_build(self):
        """Unit test for `EventBrokerFlow().build(...)`."""
        with pytest.raises(NotImplementedError):
            self.instance.build()

    @mock.patch.object(EventBrokerFlow, "execute")
    def test_execute(self, mock_execute):
        """Unit test for `EventBrokerFlow().execute(...)`."""
        mock_execute.return_value = None

        assert self.instance.execute(flow="someFlow") is None

    @mock.patch.object(EventBrokerFlow, "run")
    def test_run(self, mock_run):
        """Unit test for `EventBrokerFlow().run(...)`."""
        mock_run.return_value = None

        assert self.instance.run() is None


class TestUpcomingEventsFlow(TestCase):
    """Unit Test Cases for UpcomingEventsFlow."""

    def setUp(self) -> None:
        """Instantiate UpcomingEventsFlow."""
        self.test_flow = UpcomingEventsFlow()

    def test_build(self):
        """Unit test for `UpcomingEventsFlow.build(...)`."""
        result = self.test_flow.build(
            sport="19"
        )

        assert isinstance(result, Flow)
        assert result.name == 'betfund-bet365-upcoming-events-flow'
        assert result.schedule is None

    def test_build_with_schedule(self):
        """Unit test for `UpcomingEventsFlow.build(...)` with schedule."""
        self.test_flow.scheduled = True
        result = self.test_flow.build(
            sport="19"
        )

        assert result.schedule is not None
