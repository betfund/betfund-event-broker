"""Prefect Flow For Upcoming Events ETL."""
import os
from datetime import timedelta

from prefect import Flow, Parameter
from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock

from betfund_event_broker.flows.base_flow import EventBrokerFlow
from betfund_event_broker.tasks.bet365 import Bet365UpcomingEvents
from betfund_event_broker.tasks.helpers import Bet365UpcomingEventsStaging
from betfund_event_broker.tasks.mongo import MongoEventsUpsert


class UpcomingEventsFlow(EventBrokerFlow):
    """
    Flow for collecting all upcoming events and insert into MongoDB.

    UpcomingEventsFlow implements `build(...)`
    Consisting of 3 tasks:
        Bet365UpcomingEvents(Task)
        Bet365UpcomingEventsStaging(Task)
        MongoInsertMany(Task)

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
        """
        schedule = Schedule(
            clocks=[
                IntervalClock(
                    interval=timedelta(
                        seconds=int(
                            os.getenv("UPCOMING_EVENTS_INTERVAL", "10800")
                        )
                    ),
                )
            ]
        )

        bet365_upcoming_events = Bet365UpcomingEvents()
        upcoming_events_staging = Bet365UpcomingEventsStaging()
        mongo_events_upsert = MongoEventsUpsert()

        with Flow("betfund-bet365-upcoming-events-flow") as flow:
            sport = Parameter("sport")

            # Using Prefect's Imperative API
            # Dependencies are set with `keyword_tasks`
            # A `keyword_task` is a result of a task...
            # ...that is a dependency of the `task`

            if self.scheduled:
                flow.schedule = schedule

            flow.set_dependencies(
                task=bet365_upcoming_events,
                keyword_tasks=(dict(sport=sport)),
                mapped=True,
            )

            flow.set_dependencies(
                task=upcoming_events_staging,
                keyword_tasks=(dict(bet365_response=bet365_upcoming_events)),
                mapped=True,
                upstream_tasks=[bet365_upcoming_events],
            )

            flow.set_dependencies(
                task=mongo_events_upsert,
                keyword_tasks=(dict(documents=upcoming_events_staging)),
                mapped=True,
                upstream_tasks=[
                    bet365_upcoming_events,
                    upcoming_events_staging
                ],
            )

        return flow
