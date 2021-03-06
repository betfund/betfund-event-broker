"""Baseclass Module allowing easy execution of Flows."""
from abc import ABC, abstractmethod

from dask.distributed import Client
from prefect import Flow
from prefect.engine.executors import DaskExecutor


class EventBrokerFlow(ABC):
    """
    Higher level object for `Flow` construction and execution.

    Args:
        distributed (bool): Indication if flow should use Dask executor.
        scheduled (bool): Indication if flow has schedule.

    To minimize duplication of code we enact `EventBrokerFlow`
    EvenBrokerFlow has 1 abstract method:
    `build(...)`
        Through the build method we can construct a Flow
        Using the imperative API tasks are registered with `upstream_tasks`
        This ensures upstream tasks are finished before executing a task

    EventBrokerFlow has 2 concrete methods:
    `execute(...)`
        Through the execute method we use the builtin `run(...)` for a `Flow`
        For subclasses of Task - this will execute the constructed Flow

    `run(...)`
        Through the run method the Flow is built and executed: `Flow.run(...)`
        `run(...)` will execute all reference tasks in the Flow
        The State of each task is tracked via `State` and returned as a `dict`

    Returns:
        State: Completed state of Prefect FLow
    """

    def __init__(
        self,
        distributed: bool = False,
        scheduled: bool = False
    ):
        """Constructor for EventBrokerFlow."""
        self.distributed = distributed
        self.scheduled = scheduled

    @abstractmethod
    def build(self, *args, **kwargs):
        """
        Abstractmethod to be implemented by Subclass.

        Builds a flow via imperative API.
        (e.g.)
        ```python
        with Flow('My Imperative Flow') as flow:
            plus_one = PlusOneTask()

            flow.set_dependencies(
                task=plus_one,
                upstream_tasks=[RunMeFirst()],
                keyword_tasks=dict(x=10))
            )

            return flow
        ```

        Returns:
            Flow: Prefect Flow
        """
        raise NotImplementedError

    def execute(
        self, flow: Flow, executor=None, *args, **kwargs
    ):  # pylint: disable=W1113
        """
        Executor of EventBrokerFlow

        Through the execute method we use the builtin `run(...)` for a `Flow`
        For subclasses of Task - this will execute the constructed Flow

        Returns:
            State: State of reference tasks in Prefect Flow
        """
        flow_state = flow.run(
            executor=executor, run_on_schedule=self.scheduled, *args, **kwargs
        )

        return flow_state

    def register(self, *args, **kwargs):
        """Registers the flow to Prefect Cloud."""
        flow = self.build(*args, **kwargs)
        flow.register()

    def run(self, *args, **kwargs):
        """
        Main runner for an EventBrokerFlow.

        The flow is built via `build(...)`
            Tasks are added to the flow via Imperative API
            Setting dependencies and upstream tasks is handled

        The flow is executed via `.execute(...)`
            Flow contains builtin `.run(...)`
            The schedule is instantiated with a schedule

        Returns:
            State: State of reference tasks in Prefect Flow
        """
        flow = self.build(*args, **kwargs)

        if self.distributed:
            # Build Dask Client and Executor
            client = Client(n_workers=4, threads_per_worker=1)
            executor = DaskExecutor(address=client.scheduler.address)

            self.execute(flow=flow, executor=executor, *args, **kwargs)

        else:
            self.execute(flow=flow, *args, **kwargs)
