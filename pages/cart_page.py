from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage


class CartPage(BasePage):
    path = "/cart.html"

    def __init__(self, page):
        super().__init__(page)
        self.items = page.get_by_test_id("inventory-item")
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.checkout_button = page.get_by_test_id("checkout")

    def names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def checkout(self) -> CheckoutPage:
        self.checkout_button.click()
        return CheckoutPage(self.page)
