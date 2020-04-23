"""Command Line Interface for Running Flows."""
import click
from betfund_bet365 import Bet365SportId

from betfund_event_broker.flows import UpcomingEventsFlow


@click.command()
@click.option("-s", "--sports", is_flag=True, help="Run for all sports.")
def run(sports=True):
    """Running CLI for UpcomingEventsFlow."""
    upcoming_events = UpcomingEventsFlow()
    if sports:
        upcoming_events.run(sport=Bet365SportId.list())
