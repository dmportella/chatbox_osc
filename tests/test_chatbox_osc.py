"""Tests for Chatbox OSC."""

import pytest


def test_content(response):
    """Sample pytest test function with a pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitLab' in BeautifulSoup(response.content).title.string

@pytest.mark.local
def test_content_local(response):
    """Sample pytest test function with a pytest local" marker.

    This pytest marker can be added to your test functions to ignore this test in our GitLab pipelines.
    """
    # from bs4 import BeautifulSoup
    # assert 'GitLab' in BeautifulSoup(response.content).title.string
