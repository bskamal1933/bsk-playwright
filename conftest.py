"""Root conftest: CLI options, environment config, shared fixtures and hooks."""
from pathlib import Path

import pytest

from config.settings import Config

ROOT = Path(__file__).parent


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Target environment: a file name in config/environments (qa, staging)",
    )


def pytest_configure(config):
    (ROOT / "reports").mkdir(exist_ok=True)


def pytest_collection_modifyitems(items):
    """Tag tests with ui/api markers based on folder, so `-m api` just works."""
    for item in items:
        path = Path(str(item.fspath)).as_posix()
        if "/tests/ui/" in path:
            item.add_marker(pytest.mark.ui)
        elif "/tests/api/" in path:
            item.add_marker(pytest.mark.api)


@pytest.fixture(scope="session")
def config(pytestconfig) -> type[Config]:
    """Load the environment once per session (per xdist worker)."""
    return Config.load(pytestconfig.getoption("--env"))


@pytest.fixture(scope="session")
def base_url(config) -> str:
    """Overrides pytest-base-url. page.goto("/cart.html") resolves against this."""
    return config.ui_base_url
