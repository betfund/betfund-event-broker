"""Command Line Interface for Running Flows."""
import functools

import click
from betfund_bet365 import Bet365SportId

from betfund_event_broker.flows import UpcomingEventsFlow


@click.group()
def broker():
    """Betfund Event Broker Command Line Interface"""
    return


def flow_options(func):
    """Enable reusable click.options via `flow_options`."""
    options = [
        click.option(
            "-d", "--distributed", is_flag=True, help="Run distributed."
        ),
        click.option(
            "-s", "--scheduled", is_flag=True, help="Run on schedule."
        )
    ]
    return functools.reduce(lambda opt, option: option(opt), options, func)


@broker.command("events-register")
@flow_options
def register(distributed=False, scheduled=False):
    """Register UpcomingEventsFlow."""
    upcoming_events = UpcomingEventsFlow(
        distributed=distributed, scheduled=scheduled
    )

    upcoming_events.register()


@broker.command("events-run")
@flow_options
def run(distributed=False, scheduled=False):
    """Run UpcomingEventsFlow."""
    upcoming_events = UpcomingEventsFlow(
        distributed=distributed, scheduled=scheduled
    )

    upcoming_events.run(sport=Bet365SportId.list())
