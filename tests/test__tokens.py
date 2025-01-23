import os
import http
import pytest
from loguru import logger
import pytest_check as checks
from airgap_api.data import ErrorListResponseModel


pytestmark = [pytest.mark.api, pytest.mark.tokens]


def test__tokens__valid_credentials(ag_api_client):
    """
    Tests the tokens POST endpoint to get the user token using provided email and password.
    Steps:

    1. Perform call to tokens POST API endpoint.
    2. Verify response status code.
    3. Verify response token matches expected.
    """
    logger.info("1. Perform call to tokens POST API endpoint.")
    response = ag_api_client.tokens.get(email=os.environ["AIRGAP_EMAIL"], password=os.environ["AIRGAP_PASSWORD"])
    logger.info("2. Verify response status code.")
    assert response.status_code == http.HTTPStatus.OK
    token = response.json()["token"]
    logger.info("3. Verify response token matches expected.")
    checks.equal(token, os.environ["AIRGAP_TOKEN"])


def test__tokens__invalid_credentials(ag_api_client):
    """
    Tests the tokens POST endpoint to get the user token using provided email and password.
    Steps:

    1. Perform call to tokens POST API endpoint with invalid credentials.
    2. Verify response status code.
    3. Verify format of error response against model.
    4. Verify error data content matches expected.
    """
    logger.info("1. Perform call to tokens POST API endpoint with invalid credentials.")
    response = ag_api_client.tokens.get(email="Invalid", password="Invalid")
    logger.info("2. Verify response status code.")
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    logger.info("3. Verify format of error response against model.")
    errors = ErrorListResponseModel(**response.json())
    logger.info("4. Verify error data content matches expected.")
    checks.equal(errors.errors[0].status, "401")
    checks.equal(errors.errors[0].title, "Unauthorised")
    checks.equal(errors.errors[0].detail, "You are not authorized to perform the requested action.")
