# betfund-event-broker

<a href="https://github.com/betfund/betfund-event-broker"><img alt="GitHub Actions status" src="https://github.com/betfund/betfund-event-broker/workflows/Betfund%20Event%20Broker/badge.svg?"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

Intermediary between Bet365 and Downstream Data Processing

## Installation

From source
```bash
$ git clone https://github.com/betfund/betfund-event-broker.git
$ cd betfund-event-broker

$ python3.7 -m venv venv
$ pip install -e .
```

## Design/Usage
Implementation of Prefect `Task` for `betfund-bet365`
```python
# Using a Bet365 Base Class
from betfund_event_broker.tasks.bet365 import Bet365Task

class Bet365UpcomingEvents(Bet365Task):
    """Executes GET request to `Test` endpoint."""

    def run(self, test_arg: str):
        """
        Executes API Request to `test_endpoint(...)` endpoint.

        Args:
            test_arg (str): A test argument

        Returns:
            tuple: contains API response object and kafka topic
        """
        bet365_client = self._build_client()
        response = bet365_client.upcoming_events(test_arg=test_arg)

        return response
```

Implementation of Prefect `Flow` for a `betfund-event`
```python
from betfund_event_broker.flows.base_flow import EventBrokerFlow
from prefect import Flow

class TestFlow(EventBrokerFlow):
    """The Test FLow for EventBrokerFlow"""

    def build(self, *args, **kwargs):
        """Builds a flow via imperative API."""
        plus_one = PlusOneTask()

        with Flow("my-Imperative-flow") as flow:
            flow.set_dependencies(
                task=plus_one,
                upstream_tasks=[RunMeFirst()],
                keyword_tasks=dict(x=10)),
                mapped=False
            )

        return flow
```

## Flows
### `UpcomingEventsFlow`

Workflow Diagram:
* Fetch upcoming events and insert into NoSQL Datastore

<p align="center">
  <img width="506", height="520" src="https://imgur.com/iN6ybqz.png">


### `PreMatchOddsFlow`

Workflow Diagram:
* Fetch pre match odds lines and update `data.odds` in NoSQL Datastore

<p align="center">
  <img width="426", height="640" src="https://imgur.com/t3RVAnw.png">
  


## Command Line Interface
### A CLI is available via `event-broker`
```bash
event-broker --help

Usage: event-broker [OPTIONS] COMMAND [ARGS]...

  Betfund Event Broker Command Line Interface

Options:
  --help  Show this message and exit.

Commands:
  prematch-odds-register    Register PreMatchOddsFlow.
  prematch-odds-run         Run PreMatchOddsFlow.
  upcoming-events-register  Register UpcomingEventsFlow.
  upcoming-events-run       Run UpcomingEventsFlow.
```

### To run or register `UpcomingEventsFlow`
`event-broker upcoming-events-run`
```bash
Usage: event-broker events-run [OPTIONS]

  Run UpcomingEventsFlow.

Options:
  -s, --scheduled    Run on schedule.
  -d, --distributed  Run distributed.
  --help             Show this message and exit.
```

`event-broker events-register`
```bash
Usage: event-broker upcoming-events-register [OPTIONS]

  Register UpcomingEventsFlow.

Options:
  -s, --scheduled    Run on schedule.
  -d, --distributed  Run distributed.
  --help             Show this message and exit.
```

## Environment Variables

Bet365 API Host
- `export BET365_HOST=${BET365_HOST}`

Bet365 API Key
- `export BET365_KEY=${BET365_KEY}`

MongoDB Connection String
- `export MONGO_CONNECTION=${MONGO_CONNECTION_STRING}`

**[OPTIONAL]** Prefect Schedule Interval
- `export PREFECT_INTERVAL=${PREFECT_INTERVAL}`


## Testing
```bash
pip install -e ".[testing]"

# Test with pytest
make tests

# Lint with flake8
make flake

# Lint with pylint
make lint
```
