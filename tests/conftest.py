import os

import pytest
import markdown
from airgap_api.api.airportgap_api_client import AirportGapAPIClient


@pytest.fixture()
def ag_api_client():
    yield AirportGapAPIClient()


@pytest.fixture()
def airgap_token():
    yield os.environ["AIRGAP_TOKEN"]


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    cells.insert(2, '<th>Test Description</th>')


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    custom_description = getattr(report, "custom_description", "")
    cells.insert(2, f"<td>{markdown.markdown(custom_description)}</td>")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    outcome._result.custom_description = item.function.__doc__ or ""

