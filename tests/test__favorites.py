import http
import pytest
from loguru import logger
import pytest_check as checks
from airgap_api.data import FavoriteAirportDataPageResponse, FavoriteModel, Airports, ErrorListResponseModel


pytestmark = [pytest.mark.api, pytest.mark.favorites]


def xtest__favorites__get_initial_page(ag_api_client, airgap_token):
    """
    Tests the favorites endpoint to get first page of favorites.
    Steps:

    1. Perform call to favorites API endpoint.
    2. Verify response status code.
    3. Verify number of data items in response matches expected.
    4. Verify response data against model.
    """
    logger.info("1. Perform call to favorites API endpoint.")
    response = ag_api_client.favorites.add(airport_id=Airports.MAG.id, token=airgap_token)
    assert response.status_code in [http.HTTPStatus.CREATED, http.HTTPStatus.UNPROCESSABLE_ENTITY]

    response = ag_api_client.favorites.get(token=airgap_token)
    logger.info("2. Verify response status code.")
    assert response.status_code == http.HTTPStatus.OK

    response_data = response.json()["data"]
    # logger.info("3. Verify number of data items in response matches expected.")
    # assert len(response_data) == MAX_ITEMS_PER_PAGE
    # logger.info("4. Verify response data against model.")
    # AirportDataPageResponse.validate_python(response_data)
    assert False


def test__favorites__remove_all(ag_api_client, airgap_token):
    """
    Tests the favorites endpoint to get first page of favorites.
    Steps:

    1. Perform call to favorites API endpoint.
    2. Verify response status code.
    3. Verify number of data items in response matches expected.
    4. Verify response data against model.
    """
    # get your favs
    response = ag_api_client.favorites.get(token=airgap_token)
    favorites = response.json()["data"]
    if favorites:
        logger.info("Favorites are populated with Airports")
        f_m = FavoriteAirportDataPageResponse.validate_python(favorites)
        favorite = f_m[0]
    else:
        logger.info("Adding a favorite Airport.")
        logger.info("1. Prep: Perform call to add a favorite Airport.")
        response = ag_api_client.favorites.add(airport_id=Airports.MAG.id, token=airgap_token)
        assert response.status_code == http.HTTPStatus.CREATED

        favorite = FavoriteModel(**response.json()["data"])
    logger.debug(f"Working with favorite id: {favorite.id}")
    logger.info("2. Verify favorite is listed in response")
    response = ag_api_client.favorites.get_by_id(fav_id=favorite.id, token=airgap_token)
    assert response.status_code == http.HTTPStatus.OK
    FavoriteModel(**response.json()["data"])

    logger.info("1. Perform call to favorites API endpoint.")
    response = ag_api_client.favorites.remove_all(token=airgap_token)

    logger.info("2. Verify response status code.")
    assert response.status_code == http.HTTPStatus.NO_CONTENT

    response = ag_api_client.favorites.get_by_id(fav_id=favorite.id, token=airgap_token)
    assert response.status_code == http.HTTPStatus.NOT_FOUND

    logger.info("3. Verify format of data against model.")
    errors = ErrorListResponseModel(**response.json())
    logger.info("4. Verify data content matches expected.")
    checks.equal(errors.errors[0].status, "404")
    checks.equal(errors.errors[0].title, "Not Found")
    checks.equal(errors.errors[0].detail, "The page you requested could not be found")
