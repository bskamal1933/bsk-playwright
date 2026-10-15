from pages.base_page import BasePage


class CheckoutPage(BasePage):
    path = "/checkout-step-one.html"

    def __init__(self, page):
        super().__init__(page)
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")
        self.finish_button = page.get_by_test_id("finish")
        self.error = page.get_by_test_id("error")
        self.complete_header = page.get_by_test_id("complete-header")

    def fill_details(self, first: str, last: str, postal_code: str) -> "CheckoutPage":
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal_code)
        self.continue_button.click()
        return self

    def finish(self) -> "CheckoutPage":
        self.finish_button.click()
        return self
