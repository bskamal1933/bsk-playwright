import pytest

from test_data.factories import build_booking
from utils.schema import assert_schema


@pytest.mark.smoke
def test_create_booking(booking_api, auth_token, booking_payload):
    response = booking_api.create_booking(booking_payload)
    body = response.json()
    try:
        assert response.status == 200
        assert_schema(body, "create_booking_response.json")
        assert_schema(body["booking"], "booking.json")
        assert body["booking"] == booking_payload
    finally:
        if "bookingid" in body:
            booking_api.delete_booking(body["bookingid"], auth_token)


def test_get_booking_returns_created_data(booking_api, created_booking):
    booking_id, payload = created_booking

    response = booking_api.get_booking(booking_id)

    assert response.status == 200
    assert_schema(response.json(), "booking.json")
    assert response.json() == payload


def test_filter_booking_ids_by_name(booking_api, created_booking):
    booking_id, payload = created_booking

    response = booking_api.get_booking_ids(firstname=payload["firstname"], lastname=payload["lastname"])

    assert response.status == 200
    assert booking_id in [b["bookingid"] for b in response.json()]


def test_full_update_with_put(booking_api, auth_token, created_booking):
    booking_id, _ = created_booking
    new_payload = build_booking()

    response = booking_api.update_booking(booking_id, new_payload, auth_token)

    assert response.status == 200
    assert response.json() == new_payload
    assert booking_api.get_booking(booking_id).json() == new_payload


def test_partial_update_with_patch(booking_api, auth_token, created_booking):
    booking_id, original = created_booking
    changes = {"firstname": "Kamal", "totalprice": 999}

    response = booking_api.patch_booking(booking_id, changes, auth_token)

    assert response.status == 200
    assert response.json() == {**original, **changes}  # untouched fields stay the same


def test_delete_booking(booking_api, auth_token, created_booking):
    booking_id, _ = created_booking

    assert booking_api.delete_booking(booking_id, auth_token).status == 201
    assert booking_api.get_booking(booking_id).status == 404


@pytest.mark.parametrize("token", [None, "invalid-token"], ids=["no-token", "bad-token"])
def test_update_requires_valid_token(booking_api, created_booking, token):
    booking_id, _ = created_booking

    response = booking_api.update_booking(booking_id, build_booking(), token)

    assert response.status == 403
