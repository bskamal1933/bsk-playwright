from playwright.sync_api import Page


class BasePage:
    """Common behaviour for all page objects.

    Rules followed by every page:
    - Locators are defined once, in __init__ (they are lazy: nothing is
      searched until an action or assertion runs).
    - Page methods perform actions and return data or the next page.
    - Assertions live in tests, not in page objects.
    """

    path = "/"

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(self.path)  # relative to base_url from conftest
        return self
