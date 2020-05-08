"""Prefect Flow For Upcoming Events ETL."""
import os
from datetime import timedelta

from prefect import Flow, unmapped
from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock

from betfund_event_broker.flows.base_flow import EventBrokerFlow
from betfund_event_broker.tasks.bet365 import Bet365PreMatchOdds
from betfund_event_broker.tasks.helpers import PointInTime
from betfund_event_broker.tasks.mongo import MongoFindEvents


class PreMatchOddsFlow(EventBrokerFlow):
    """
    Flow for query and collection of pre-match odds lines.

    PreMatchOddsFlow implements `build(...)`
    Consisting of 3 tasks:
        Bet365PreMatchOdds(Task)

    Args:
        fi (str): Bet365 event fi

    Returns:
        State: State of completed Prefect `Flow`

    """

    def build(self) -> Flow:
        """
        Build flow via imperative API.
        `schedule` - is an IntervalClock Prefect schedule
        This is defined by an arbitrary timedelta
        Args:
            fi (str): Bet365 event fi
        Returns:
            flow (Flow): Prefect `Flow` constructed
        """
        schedule = Schedule(
            clocks=[
                IntervalClock(
                    interval=timedelta(
                        seconds=int(os.getenv("PREFECT_INTERVAL", "30"))
                    ),
                )
            ]
        )

        point_in_time = PointInTime()
        mongo_find_events = MongoFindEvents()
        bet365_prematch_odds = Bet365PreMatchOdds()

        with Flow("betfund-bet365-prematch-odds-flow") as flow:
            # Using Prefect's Imperative API
            # Dependencies are set with `keyword_tasks`
            # A `keyword_task` is a result of a task...
            # ...that is a dependency of the `task`

            if self.scheduled:
                flow.schedule = schedule

            flow.set_dependencies(
                task=point_in_time
            )

            flow.set_dependencies(
                task=mongo_find_events,
                keyword_tasks=(dict(epoch=point_in_time))
            )

            flow.set_dependencies(
                task=bet365_prematch_odds,
                keyword_tasks=(dict(documents=mongo_find_events)),
                mapped=True,
                upstream_tasks=[mongo_find_events, unmapped(point_in_time)],
            )

        return flow
