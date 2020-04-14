.PHONY: black
black:
	black betfund_event_broker

.PHONY: tests
tests:
	pytest -vv --cov=betfund_event_broker --cov-report term-missing

.PHONY: lint
lint:
	pylint betfund_event_broker/

.PHONY: flake
flake:
	flake8 betfund_event_broker

.PHONY: isort
isort:
	isort --recursive betfund_event_broker/ tests/