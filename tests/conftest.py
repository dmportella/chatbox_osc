"""Pytest configuration file for Chatbox OSC."""

import pytest


def pytest_configure(config):
    # A "local" marker to ignore tests that will fail in the Gitlab pipelines
    # Add `@pytest.mark.local` above your tests functions you want to ignore online
    config.addinivalue_line("markers", "local : mark a local test")

@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://gitlab.com/ameliend/python-package-cookiecutter-template')
