import http
import pytest
from loguru import logger
import pytest_check as checks
from airgap_api.data import FavoriteAirportDataPageResponse, FavoriteModel, Airports, ErrorListResponseModel


pytestmark = [pytest.mark.api, pytest.mark.favorites]


def test__favorites__get_initial_page(ag_api_client, airgap_token):
    """
    Tests the favorites endpoint to get first page of favorites.
    Steps:

    1. Perform call to favorites API endpoint.
    2. Verify response status code.
    """
    logger.info("1. Perform call to favorites API endpoint.")
    response = ag_api_client.favorites.get(token=airgap_token)
    logger.info("2. Verify response status code.")
    assert response.status_code == http.HTTPStatus.OK


def test__favorites__remove_all(ag_api_client, airgap_token):
    """
    Tests the favorites endpoint to remove all Airports from favorites.
    Steps:

    1. Get all current favorites.
    2. Ensure favorites contain an Airport
    2.1. Adding an Airport to favorites.
    3. Verify specific Airport is contained within the favorites.
    4. Perform call to remove all favorites API endpoint.
    5. Expect specific Airport to not be in favorites.
    6. Verify format of error data against model.
    """
    logger.info("1. Get all current favorites.")
    response = ag_api_client.favorites.get(token=airgap_token)
    favorites = response.json()["data"]
    logger.info("2. Ensure favorites contain an Airport.")
    if favorites:
        f_m = FavoriteAirportDataPageResponse.validate_python(favorites)
        favorite = f_m[0]
    else:
        logger.info("2.1. Adding an Airport to favorites.")
        response = ag_api_client.favorites.add(airport_id=Airports.MAG.id, token=airgap_token)
        assert response.status_code == http.HTTPStatus.CREATED
        favorite = FavoriteModel(**response.json()["data"])

    logger.debug(f"Working with favorite id: {favorite.id}")
    logger.info("3. Verify specific Airport is contained within the favorites.")
    response = ag_api_client.favorites.get_by_id(fav_id=favorite.id, token=airgap_token)
    assert response.status_code == http.HTTPStatus.OK
    FavoriteModel(**response.json()["data"])

    logger.info("4. Perform call to remove all favorites API endpoint.")
    response = ag_api_client.favorites.remove_all(token=airgap_token)
    assert response.status_code == http.HTTPStatus.NO_CONTENT

    logger.info("5. Expect specific Airport to not be in favorites.")
    response = ag_api_client.favorites.get_by_id(fav_id=favorite.id, token=airgap_token)
    assert response.status_code == http.HTTPStatus.NOT_FOUND

    logger.info("6. Verify format of error data against model.")
    errors = ErrorListResponseModel(**response.json())
    checks.equal(errors.errors[0].status, "404")
    checks.equal(errors.errors[0].title, "Not Found")
    checks.equal(errors.errors[0].detail, "The page you requested could not be found")


def test__favorites__remove_single(ag_api_client, airgap_token):
    """
    Tests the favorites endpoint to remove a specific Airport from favorites.
    Steps:

    1. Get all current favorites.
    2. Ensure favorites contain an Airport
    2.1. Adding an Airport to favorites.
    3. Verify specific Airport is contained within the favorites.
    4. Perform call to remove specific favorite API endpoint.
    5. Expect specific Airport to not be in favorites.
    6. Verify format of error data against model.
    """
    logger.info("1. Get all current favorites.")
    response = ag_api_client.favorites.get(token=airgap_token)
    favorites = response.json()["data"]
    logger.info("2. Ensure favorites contain an Airport.")
    if favorites:
        f_m = FavoriteAirportDataPageResponse.validate_python(favorites)
        favorite = f_m[0]
    else:
        logger.info("2.1. Adding an Airport to favorites.")
        response = ag_api_client.favorites.add(airport_id=Airports.MAG.id, token=airgap_token)
        assert response.status_code == http.HTTPStatus.CREATED
        favorite = FavoriteModel(**response.json()["data"])

    logger.debug(f"Working with favorite id: {favorite.id}")
    logger.info("3. Verify specific Airport is contained within the favorites.")
    response = ag_api_client.favorites.get_by_id(fav_id=favorite.id, token=airgap_token)
    assert response.status_code == http.HTTPStatus.OK
    FavoriteModel(**response.json()["data"])

    logger.info("4. Perform call to remove specific favorite API endpoint.")
    response = ag_api_client.favorites.remove(token=airgap_token, fav_id=favorite.id)
    assert response.status_code == http.HTTPStatus.NO_CONTENT

    logger.info("5. Expect specific Airport to not be in favorites.")
    response = ag_api_client.favorites.get_by_id(fav_id=favorite.id, token=airgap_token)
    assert response.status_code == http.HTTPStatus.NOT_FOUND

    logger.info("6. Verify format of error data against model.")
    errors = ErrorListResponseModel(**response.json())
    checks.equal(errors.errors[0].status, "404")
    checks.equal(errors.errors[0].title, "Not Found")
    checks.equal(errors.errors[0].detail, "The page you requested could not be found")


def test__favorites__update_note(ag_api_client, airgap_token):
    """
    Tests the favorites endpoint to update the note on a specific Airport from favorites.
    Steps:

    1. Get all current favorites.
    2. Ensure favorites contain an Airport
    2.1. Adding an Airport to favorites.
    3. Verify specific Airport is contained within the favorites.
    4. Perform call to update the note.
    5. Get note from favorites.
    """
    logger.info("1. Get all current favorites.")
    response = ag_api_client.favorites.get(token=airgap_token)
    favorites = response.json()["data"]
    logger.info("2. Ensure favorites contain an Airport.")
    if favorites:
        f_m = FavoriteAirportDataPageResponse.validate_python(favorites)
        favorite = f_m[0]
    else:
        logger.info("2.1. Adding an Airport to favorites.")
        response = ag_api_client.favorites.add(airport_id=Airports.MAG.id, token=airgap_token)
        assert response.status_code == http.HTTPStatus.CREATED
        favorite = FavoriteModel(**response.json()["data"])

    logger.debug(f"Working with favorite id: {favorite.id}")
    logger.info("3. Verify specific Airport is contained within the favorites.")
    response = ag_api_client.favorites.get_by_id(fav_id=favorite.id, token=airgap_token)
    assert response.status_code == http.HTTPStatus.OK
    FavoriteModel(**response.json()["data"])
    current_note = favorite.attributes.note
    logger.debug(f"Note on favorite {favorite.id} is {current_note}")

    logger.info("4. Perform call to update the note.")
    response = ag_api_client.favorites.update_note(token=airgap_token, fav_id=favorite.id, note="One of the best")
    assert response.status_code == http.HTTPStatus.OK

    logger.info("5. Get note from favorites.")
    response = ag_api_client.favorites.get_by_id(fav_id=favorite.id, token=airgap_token)
    assert response.status_code == http.HTTPStatus.OK
    updated_note = FavoriteModel(**response.json()["data"]).attributes.note
    checks.not_equal(updated_note, current_note)
    checks.equal(updated_note, "One of the best")
