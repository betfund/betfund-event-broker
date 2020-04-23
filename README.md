# betfund-event-broker
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
  <img width="566", height="520" src="https://imgur.com/TQOT11f.png">
 

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