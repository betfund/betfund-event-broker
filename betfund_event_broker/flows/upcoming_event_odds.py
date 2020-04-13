"""Prefect Flow Builder."""
import os
from datetime import timedelta

from prefect import Flow, Parameter
from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock

from betfund_bet365 import Bet365SportId
from betfund_event_broker.flows.base import EventBrokerFlow
from betfund_event_broker.tasks.bet365.prematch_odds import Bet365PreMatchOdds
from betfund_event_broker.tasks.bet365.upcoming_events import Bet365UpcomingEvents
from betfund_event_broker.tasks.pykafka.producer import EventProducer


class UpcomingEventOddsFlow(EventBrokerFlow):
    """
    Flow for collecting all upcoming events and push to Kafka.

    UpcomingEventOddsFlow implements `build(...)`

    Args:
        sport (str): Sport identifier for Bet365 request.

    Returns:
        State: State of completed Prefect `Flow`

    """

    def build(self, sport: tuple) -> Flow:
        """
        Build flow via imperative API.
        `schedule` - is an IntervalClock Prefect schedule
        This is defined by an arbitrary timedelta
        Args:
            sport (str): Sport identifier for Bet365 request.
        Returns:
            flow (Flow): Prefect `Flow` constructed
            `flow` consists of 3 subclasses of `Task`
                Bet365UpcomingEvents(Task)
        """
        schedule = Schedule(
            clocks=[
                IntervalClock(
                    interval=timedelta(
                        seconds=int(os.getenv("PREFECT_INTERVAL", "20"))
                    ),
                )
            ]
        )

        bet365_pre_match_odds = Bet365PreMatchOdds()
        bet365_upcoming_events = Bet365UpcomingEvents()
        kafka_producer = EventProducer()

        with Flow("betfund-bet365-upcoming-events-flow") as flow:
            sport = Parameter("sport")

            # Using Prefect's Imperative API
            # Dependencies are set with `keyword_tasks`
            # A `keyword_task` is a result of a task...
            # ...that is a dependency of the `task`

            flow.schedule = schedule
            flow.set_dependencies(
                task=bet365_upcoming_events,
                keyword_tasks=(dict(sport=sport)),
                mapped=True
            )

            flow.set_dependencies(
                task=bet365_pre_match_odds,
                keyword_tasks=(dict(fi=bet365_upcoming_events)),
                mapped=True,
                upstream_tasks=[bet365_upcoming_events]
            )

            flow.set_dependencies(
                task=kafka_producer,
                mapped=True,
                keyword_tasks=dict(asset=bet365_pre_match_odds),
                upstream_tasks=[bet365_pre_match_odds],
            )

        return flow
