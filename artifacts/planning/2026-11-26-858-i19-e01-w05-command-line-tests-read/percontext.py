"""Pytest plugin: switch the coverage context to each test's node id."""

import coverage
import pytest


def _switch(name: str) -> None:
    current = coverage.Coverage.current()
    if current is not None:
        current.switch_context(name)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):  # type: ignore[no-untyped-def]
    _switch(item.nodeid)
    yield
    _switch("")
