"""UI fixtures: locator setup, test data, and login reuse via storage_state."""
import pytest
from playwright.sync_api import expect

from pages import InventoryPage, LoginPage
from test_data.loader import load_json


@pytest.fixture(scope="session", autouse=True)
def _test_id_attribute(playwright):
    """The demo app uses data-test="..." instead of the default data-testid."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session", autouse=True)
def _expect_timeout(config):
    expect.set_options(timeout=config.timeout_ms)


@pytest.fixture(scope="session")
def users() -> dict:
    return load_json("users.json")


@pytest.fixture(scope="session")
def products() -> dict:
    return load_json("products.json")


@pytest.fixture(scope="session")
def auth_state(browser, base_url, users, tmp_path_factory, _test_id_attribute):
    """Log in ONCE per session (per xdist worker) and save cookies + storage.

    Tests that need a logged-in user load this file instead of repeating the
    login steps, which is faster and keeps login failures out of unrelated tests.
    """
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    LoginPage(page).open().login_as(users["standard"])
    page.wait_for_url("**/inventory.html")
    path = tmp_path_factory.mktemp("auth") / "standard_user.json"
    context.storage_state(path=path)
    context.close()
    return path


@pytest.fixture
def login_page(page) -> LoginPage:
    """Fresh, logged-out context (pytest-playwright gives one per test)."""
    return LoginPage(page).open()


@pytest.fixture
def inventory_page(new_context, auth_state) -> InventoryPage:
    """Already logged in. new_context still records traces/videos on failure."""
    context = new_context(storage_state=auth_state)
    page = context.new_page()
    return InventoryPage(page).open()
