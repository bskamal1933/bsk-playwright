import pytest


@pytest.mark.smoke
def test_health_check(booking_api):
    assert booking_api.health().status == 201


@pytest.mark.smoke
def test_valid_credentials_return_token(booking_api, config):
    response = booking_api.create_token(config.api_username, config.api_password)

    assert response.status == 200
    token = response.json()["token"]
    assert isinstance(token, str) and token


def test_invalid_credentials_are_rejected(booking_api):
    response = booking_api.create_token("admin", "wrong-password")

    # Known quirk of this practice API: it returns 200 with an error body
    # instead of 401. Asserting on the body catches it either way.
    assert response.status == 200
    assert response.json() == {"reason": "Bad credentials"}
