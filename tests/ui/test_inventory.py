import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_inventory_lists_all_products(inventory_page):
    expect(inventory_page.items).to_have_count(6)


@pytest.mark.parametrize("key, descending", [("price_asc", False), ("price_desc", True)])
def test_sort_by_price(inventory_page, key, descending):
    inventory_page.sort_by(key)

    prices = inventory_page.prices()
    assert prices == sorted(prices, reverse=descending)


def test_sort_by_name_descending(inventory_page):
    inventory_page.sort_by("name_desc")

    names = inventory_page.names()
    assert names == sorted(names, reverse=True)


def test_add_and_remove_updates_cart_badge(inventory_page, products):
    inventory_page.add_to_cart(products["backpack"]).add_to_cart(products["bike_light"])
    expect(inventory_page.cart_badge).to_have_text("2")

    inventory_page.remove_from_cart(products["backpack"])
    expect(inventory_page.cart_badge).to_have_text("1")
