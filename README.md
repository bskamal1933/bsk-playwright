# Playwright Python Reference Framework

A small but complete UI + API test framework built with **Playwright (sync API) + pytest**.
It is meant as a reference: every file shows one pattern you can explain in an interview.

- **UI app under test:** [Sauce Demo](https://www.saucedemo.com) (login, inventory, cart, checkout)
- **API under test:** [Restful Booker](https://restful-booker.herokuapp.com) (token auth + booking CRUD)

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest                             # everything, qa env
pytest -m smoke                    # critical path only
pytest -m api                      # API only (no browser launched)
pytest -m ui --headed --slowmo 300 # watch the browser
pytest --env=staging               # another environment
pytest -n auto                     # parallel (pytest-xdist)
pytest --reruns 2                  # retry flaky tests (pytest-rerunfailures)
```

Open `reports/report.html` after a run. For a failed UI test, open its trace:

```bash
playwright show-trace reports/artifacts/<test-folder>/trace.zip
```

## Project structure

```
├── conftest.py                 # --env option, Config loading, base_url, auto ui/api markers
├── pytest.ini                  # markers, report, screenshot/video/trace on failure
├── requirements.txt
├── config/
│   ├── settings.py             # Config class: @classmethod load(env)
│   └── environments/           # qa.json, staging.json
├── pages/                      # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── api/                        # API client layer over APIRequestContext
│   ├── base_client.py
│   └── booking_client.py
├── test_data/
│   ├── users.json, products.json   # static data
│   ├── factories.py                # Faker-based unique data
│   ├── loader.py                   # cached JSON loader (returns copies)
│   └── schemas/                    # JSON schemas for response validation
├── utils/schema.py             # assert_schema() helper
├── tests/
│   ├── ui/   conftest.py, test_login.py, test_inventory.py, test_checkout.py
│   └── api/  conftest.py, test_auth.py, test_booking_crud.py
├── reports/                    # generated: report.html, test.log, artifacts/
└── .github/workflows/tests.yml # CI: api + ui jobs in parallel, uploads reports
```

## Design decisions (interview talking points)

| Pattern | Where | Why |
|---|---|---|
| **Sync API** | everywhere | Test steps are sequential; pytest-xdist gives parallelism with separate processes. |
| **Browser → Context → Page** | pytest-playwright fixtures | Each test gets a fresh, isolated context; one browser per worker. |
| **Config via `@classmethod`** | `config/settings.py` | Loaded once per session into class variables; shared by all tests. Env vars override secrets. |
| **`--env` option** | root `conftest.py` | Same tests, different environments, no code change. |
| **Page Object Model** | `pages/` | Locators in one place; methods return data or the next page (fluent). No assertions in pages. |
| **User-facing locators** | `get_by_role`, `get_by_test_id` | Resilient to markup changes; `set_test_id_attribute("data-test")` matches the app. |
| **Locator filtering/chaining** | `InventoryPage.item_card()` | `items.filter(has_text=...).get_by_role("button", ...)` scopes actions to one card. |
| **Web-first assertions** | `expect(...)` in tests | Auto-retry until timeout; no sleeps. |
| **Login once with `storage_state`** | `tests/ui/conftest.py` | Session fixture logs in once and saves cookies; tests start already logged in. |
| **API client layer** | `api/` | Tests read like intent (`booking_api.create_booking`), not raw HTTP. |
| **Static method helper** | `BookingClient._auth()` | Pure helper that needs neither `self` nor `cls`. |
| **Fixtures with teardown** | `created_booking` | Arrange via API, `yield`, always clean up. |
| **Data-driven tests** | `parametrize` + `users.json` | One test, many cases, readable IDs. |
| **Unique data per test** | `factories.py` (Faker) | Safe for parallel runs; no collisions. |
| **Schema validation** | `utils/schema.py` | Catches contract changes, lists every violation. |
| **Failure artifacts** | `pytest.ini` | Screenshot, video and trace kept only for failures. |
| **CI** | GitHub Actions | API and UI suites run in parallel jobs; reports uploaded every run. |

## Notes

- Both targets are public practice sites. If one is down, its tests fail with a connection error, not a framework bug.
- Restful Booker returns `200` with `{"reason": "Bad credentials"}` for a wrong password; `test_auth.py` documents this quirk.
- Swap `config/environments/*.json` and the page/API classes to point the framework at a real app.
