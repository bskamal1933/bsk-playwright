"""Test data factories: unique, realistic data per test (safe for parallel runs)."""
from datetime import date, timedelta

from faker import Faker

fake = Faker()


def build_booking(**overrides) -> dict:
    check_in = date.today() + timedelta(days=fake.random_int(1, 30))
    check_out = check_in + timedelta(days=fake.random_int(1, 7))
    booking = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(100, 5000),
        "depositpaid": fake.boolean(),
        "bookingdates": {
            "checkin": check_in.isoformat(),
            "checkout": check_out.isoformat(),
        },
        "additionalneeds": fake.random_element(["Breakfast", "Late checkout", "Airport pickup"]),
    }
    booking.update(overrides)
    return booking


def build_customer() -> dict:
    return {
        "first": fake.first_name(),
        "last": fake.last_name(),
        "postal_code": fake.postcode(),
    }
