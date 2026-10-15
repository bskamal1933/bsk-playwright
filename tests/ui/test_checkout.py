import pytest
from playwright.sync_api import expect

from test_data.factories import build_customer


@pytest.mark.smoke
def test_end_to_end_purchase(inventory_page, products):
    cart = inventory_page.add_to_cart(products["backpack"]).open_cart()
    expect(cart.item_names).to_have_text([products["backpack"]])

    checkout = cart.checkout().fill_details(**build_customer()).finish()

    expect(checkout.complete_header).to_have_text("Thank you for your order!")


def test_checkout_requires_postal_code(inventory_page, products):
    checkout = inventory_page.add_to_cart(products["bike_light"]).open_cart().checkout()

    checkout.fill_details("Kamal", "Bharadwaj", "")

    expect(checkout.error).to_contain_text("Postal Code is required")
