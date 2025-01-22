import pytest
from loguru import logger
import pytest_check as checks
import http
from airgap_api.data import AirportDataModel, ErrorListResponseModel, Airports, AirportDistanceResultModel, AirportDataPageResponse

pytestmark = [pytest.mark.api, pytest.mark.airports]

MAX_ITEMS_PER_PAGE = 30


def test__airports__get_initial_page(ag_api_client):
    """
    Tests the airports GET endpoint to get the initial page of data.
    Steps:

    1. Perform call to airports get API endpoint.
    2. Verify response status code.
    3. Verify number of data items in response matches expected.
    4. Verify response data against model.
    """
    logger.info("1. Perform call to airports get API endpoint.")
    response = ag_api_client.airports.get()
    logger.info("2. Verify response status code.")
    assert response.status_code == http.HTTPStatus.OK
    response_data = response.json()["data"]
    logger.info("3. Verify number of data items in response matches expected.")
    assert len(response_data) == MAX_ITEMS_PER_PAGE
    logger.info("4. Verify response data against model.")
    AirportDataPageResponse.validate_python(response_data)


def test__airports__get_single_page(ag_api_client):
    """
    Tests the airports GET endpoint to get a specific page of data.
    Steps:

    1. Perform call to airports get API endpoint specifying page parameter.
    2. Verify response status code.
    3. Verify number of data items in response matches expected.
    4. Verify response data against model.
    """
    logger.info("1. Perform call to airports get API endpoint specifying page parameter.")
    response = ag_api_client.airports.get(page=2)
    logger.info("2. Verify response status code.")
    assert response.status_code == http.HTTPStatus.OK
    response_data = response.json()["data"]
    logger.info("3. Verify number of data items in response matches expected.")
    assert len(response_data) == MAX_ITEMS_PER_PAGE
    logger.info("4. Verify response data against model.")
    AirportDataPageResponse.validate_python(response_data)


def test__airports__exceed_max_page(ag_api_client):
    """
    Tests the airports GET endpoint specifying an invalid page parameter.

    Steps:
    1. Perform call to airports get API endpoint specifying invalid page parameter.
    2. Verify response status code.
    3. Verify number of data items in response matches expected.
    """
    logger.info("1. Perform call to airports get API endpoint specifying invalid page parameter.")
    response = ag_api_client.airports.get(page=2000)
    logger.info("2. Verify response status code.")
    assert response.status_code == http.HTTPStatus.OK
    expected_count = 0
    logger.info("3. Verify number of data items in response matches expected.")
    assert len(response.json()["data"]) == expected_count


def test__airports__valid_airport_id(ag_api_client):
    """
    Tests the airports GET by ID endpoint.

    Steps:
    1. Perform call to airports GET by ID API endpoint specifying valid id.
    2. Verify response status code.
    3. Verify format of data against model.
    4. Verify data content matches expected.
    """
    logger.info("1. Perform call to airports GET by ID API endpoint specifying valid id.")
    response = ag_api_client.airports.get_by_id(airport_id=Airports.MAG.id)
    logger.info("2. Verify response status code.")
    assert response.status_code == http.HTTPStatus.OK
    logger.info("3. Verify format of data against model.")
    resp_data = AirportDataModel(**response.json()["data"])
    logger.info("4. Verify data content matches expected.")
    assert resp_data == Airports.MAG


def test__airports__invalid_airport_id(ag_api_client):
    """
    Tests the airports GET by ID endpoint when invalid id is supplied.

    Steps:
    1. Perform call to airports GET by ID API endpoint specifying invalid id.
    2. Verify response status code.
    3. Verify format of data against model.
    4. Verify data content matches expected.
    """
    logger.info("1. Perform call to airports GET by ID API endpoint specifying invalid id.")
    response = ag_api_client.airports.get_by_id(airport_id="INVALID")
    logger.info("2. Verify response status code.")
    assert response.status_code == http.HTTPStatus.NOT_FOUND
    logger.info("3. Verify format of data against model.")
    errors = ErrorListResponseModel(**response.json())
    logger.info("4. Verify data content matches expected.")
    checks.equal(errors.errors[0].status, "404")
    checks.equal(errors.errors[0].title, "Not Found")
    checks.equal(errors.errors[0].detail, "The page you requested could not be found")


@pytest.mark.slow
def test__airports__all_pages(ag_api_client):
    """
    Tests the airports data returned by every page returned from GET endpoint.
    Steps:

    1. Get all pages of airport data.
    2. Verify data format of each airport.
    """
    logger.info("1. Get all pages of airport data.")
    for page_data in ag_api_client.airports.get_all():
        for airport in page_data:
            logger.info("2. Verify data format of each airport.")
            assert AirportDataModel(**airport)


@pytest.mark.wip
def test__airports__distance_calc(ag_api_client):
    """
    Tests the airports distance endpoint.
    Steps:

    1. Perform call to airports distance API endpoint.
    2. Verify response status code.
    3. Verify format of data against model.
    4. Verify data content matches expected.
    """
    from_airport = Airports.MAG
    to_airport = Airports.CYG
    logger.info("1. Perform call to airports distance API endpoint.")
    response = ag_api_client.airports.distance(from_id=from_airport.id, to_id=to_airport.id)
    logger.info("2. Verify response status code.")
    assert response.status_code == http.HTTPStatus.OK
    logger.info("3. Verify format of data against model.")
    distance_data = AirportDistanceResultModel(**response.json()["data"])
    logger.info("4. Verify data content matches expected.")
    checks.almost_equal(distance_data.attributes.kilometers, 3451.0132605573453, msg="Kilometers")
    checks.almost_equal(distance_data.attributes.miles, 2142.86743976846, msg="Miles")
    checks.almost_equal(distance_data.attributes.nautical_miles, 1862.1000015367488, msg="Nautical Miles")
