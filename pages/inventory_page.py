from pages.base_page import BasePage
from pages.cart_page import CartPage


class InventoryPage(BasePage):
    path = "/inventory.html"

    SORT_OPTIONS = {
        "name_asc": "Name (A to Z)",
        "name_desc": "Name (Z to A)",
        "price_asc": "Price (low to high)",
        "price_desc": "Price (high to low)",
    }

    def __init__(self, page):
        super().__init__(page)
        self.title = page.get_by_test_id("title")
        self.items = page.get_by_test_id("inventory-item")
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.item_prices = page.get_by_test_id("inventory-item-price")
        self.sort_dropdown = page.get_by_test_id("product-sort-container")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.cart_link = page.get_by_test_id("shopping-cart-link")

    def item_card(self, product_name: str):
        """Locator chaining + filtering: the card that contains this product."""
        return self.items.filter(has_text=product_name)

    def add_to_cart(self, product_name: str) -> "InventoryPage":
        self.item_card(product_name).get_by_role("button", name="Add to cart").click()
        return self

    def remove_from_cart(self, product_name: str) -> "InventoryPage":
        self.item_card(product_name).get_by_role("button", name="Remove").click()
        return self

    def sort_by(self, key: str) -> "InventoryPage":
        self.sort_dropdown.select_option(label=self.SORT_OPTIONS[key])
        return self

    def names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def prices(self) -> list[float]:
        return [float(p.replace("$", "")) for p in self.item_prices.all_inner_texts()]

    def open_cart(self) -> CartPage:
        self.cart_link.click()
        return CartPage(self.page)
