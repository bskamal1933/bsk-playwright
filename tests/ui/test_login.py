import re

import pytest
from playwright.sync_api import expect

from test_data.loader import load_json

INVALID_LOGINS = load_json("users.json")["invalid_logins"]


@pytest.mark.smoke
def test_valid_login_lands_on_products(login_page, users):
    inventory = login_page.login_as(users["standard"])

    expect(inventory.page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(inventory.title).to_have_text("Products")


def test_locked_out_user_sees_error(login_page, users):
    user = users["locked_out"]
    login_page.login(user["username"], user["password"])

    expect(login_page.error).to_contain_text("locked out")


@pytest.mark.parametrize("case", INVALID_LOGINS, ids=[c["id"] for c in INVALID_LOGINS])
def test_invalid_login_shows_error(login_page, case):
    login_page.login(case["username"], case["password"])

    expect(login_page.error).to_contain_text(case["error"])
    expect(login_page.page).not_to_have_url(re.compile("inventory"))
