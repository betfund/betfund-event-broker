"""A setuptools based setup module."""
from io import open
from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="betfund-event-broker",
    version="0.0.1",
    description="Intermediary between Bet365 and Spark Stream",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/betfund/betfund-event-broker",
    author="Michell Bregman, Leon Kozlowski",
    author_email="mitchbregs@gmail.com, leonkozlowski@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords="kafka spark stream",
    packages=find_packages(),
    install_requires=[
        "betfund_bet365 @ git+https://github.com/betfund/betfund-bet365.git@0.0.6",
        "betfund-logger @ git+https://github.com/betfund/betfund-logger.git@0.0.2",
        "kafka-python",
        "prefect",
        "pymongo",
        "pymongo[srv]"
    ],
    extras_require={
        "testing": [
            "black",
            "flake8",
            "isort",
            "mock",
            "pylint",
            "pytest",
            "pytest-cov"
        ]
    },
    entry_points =
        """
        [console_scripts]
        betfund-event-broker=betfund_event_broker.cli.main:run
        """
)
