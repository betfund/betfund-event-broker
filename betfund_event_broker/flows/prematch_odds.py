"""Prefect Flow For Upcoming Events ETL."""
import os
from datetime import timedelta

from prefect import Flow, unmapped
from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock

from betfund_event_broker.flows.base_flow import EventBrokerFlow
from betfund_event_broker.tasks.bet365 import Bet365PreMatchOdds
from betfund_event_broker.tasks.helpers import (
    Bet365PreMatchOddsStaging,
    PointInTime
)
from betfund_event_broker.tasks.mongo import MongoFindEvents, MongoOddsUpsert


class PreMatchOddsFlow(EventBrokerFlow):
    """
    Flow for query and collection of pre-match odds.

    PreMatchOddsFlow implements `build(...)`
    Consisting of 3 tasks:
        PointInTime(Task)
        MongoFindEvents(Task)
        Bet365PreMatchOdds(Task)
        Bet365PreMatchOddsStaging(Task)
        MongoOddsUpsert(Task)

    Returns:
        State: State of completed Prefect `Flow`

    """

    def build(self) -> Flow:
        """
        Build flow via imperative API.
        `schedule` - is an IntervalClock Prefect schedule
        This is defined by an arbitrary timedelta

        Returns:
            flow (Flow): Prefect `Flow` constructed
        """
        schedule = Schedule(
            clocks=[
                IntervalClock(
                    interval=timedelta(
                        seconds=int(
                            os.getenv("PRE_MATCH_ODDS_INTERVAL", "120")
                        )
                    ),
                )
            ]
        )

        point_in_time = PointInTime()
        mongo_find_events = MongoFindEvents()
        bet365_pre_match_odds = Bet365PreMatchOdds()
        pre_match_odds_staging = Bet365PreMatchOddsStaging()
        mongo_odds_upsert = MongoOddsUpsert()

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
                keyword_tasks=(dict(epoch=point_in_time)),
                upstream_tasks=[unmapped(point_in_time)]
            )

            flow.set_dependencies(
                task=bet365_pre_match_odds,
                keyword_tasks=(dict(document=mongo_find_events)),
                mapped=True,
                upstream_tasks=[
                    unmapped(point_in_time),
                    mongo_find_events
                ]
            )

            flow.set_dependencies(
                task=pre_match_odds_staging,
                keyword_tasks=(
                    dict(bet365_response=bet365_pre_match_odds)
                ),
                mapped=True,
                upstream_tasks=[
                    unmapped(point_in_time),
                    mongo_find_events,
                    bet365_pre_match_odds
                ]
            )

            flow.set_dependencies(
                task=mongo_odds_upsert,
                keyword_tasks=(
                    dict(attributes=pre_match_odds_staging)
                ),
                mapped=True,
                upstream_tasks=[
                    unmapped(point_in_time),
                    mongo_find_events,
                    bet365_pre_match_odds,
                    pre_match_odds_staging
                ]
            )

        return flow
