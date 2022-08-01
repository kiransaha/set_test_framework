"""
Global fixtures
"""

import pytest
from _pytest.nodes import Item
from _pytest.runner import CallInfo





def pytest_addoption(parser):
    parser.addoption(
        "--email", action="store_true", default=False, help="Send Report at end of run."
    )

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo):
    """
    - Adds test_report attribute to request object for use with failure_snapshot fixture.
    - Capture failures in the setup call and store them on our test invocation item
    :param item: Item
    :param call: CallInfo
    :return:
    """
    if call.excinfo is not None and call.when == 'setup':
        item.setup_failed = True

    outcome = yield
    rep = outcome.get_result()

    setattr(item, 'test_report', rep)
