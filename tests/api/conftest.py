"""API fixtures. No browser is launched for these tests."""
import pytest

from api import BookingClient
from test_data.factories import build_booking


@pytest.fixture(scope="session")
def api_context(playwright, config):
    context = playwright.request.new_context(
        base_url=config.api_base_url,
        extra_http_headers={"Accept": "application/json"},
    )
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def booking_api(api_context) -> BookingClient:
    return BookingClient(api_context)


@pytest.fixture(scope="session")
def auth_token(booking_api, config) -> str:
    response = booking_api.create_token(config.api_username, config.api_password)
    assert response.ok, f"Auth failed: {response.status} {response.text()}"
    token = response.json().get("token")
    assert token, f"No token in auth response: {response.text()}"
    return token


@pytest.fixture
def booking_payload() -> dict:
    return build_booking()


@pytest.fixture
def created_booking(booking_api, auth_token, booking_payload):
    """Arrange via API, yield to the test, always clean up afterwards."""
    response = booking_api.create_booking(booking_payload)
    assert response.ok, f"Setup failed: {response.status} {response.text()}"
    booking_id = response.json()["bookingid"]

    yield booking_id, booking_payload

    booking_api.delete_booking(booking_id, auth_token)  # 405 if the test already deleted it
