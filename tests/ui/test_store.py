import pytest
from pages.store_page import StorePage

pytestmark = pytest.mark.ui

def test_search_filters_product_catalog(driver, base_url):
    store = StorePage(driver, base_url).open_authenticated().search("keyboard")
    assert store.visible_products() == ["Mechanical Keyboard"]

def test_search_handles_no_results(driver, base_url):
    store = StorePage(driver, base_url).open_authenticated().search("nonexistent")
    assert store.visible_products() == []
    assert driver.find_element("id", "no-results").is_displayed()

def test_add_product_updates_cart_count_and_total(driver, base_url):
    store = StorePage(driver, base_url).open_authenticated().add_product(1)
    assert store.cart_count() == 1
    assert store.cart_total() == 89.99

def test_quantity_change_recalculates_total(driver, base_url):
    store = StorePage(driver, base_url).open_authenticated().add_product(2).set_quantity(2, 3)
    assert store.cart_count() == 3
    assert store.cart_total() == 118.50

def test_customer_can_complete_checkout(driver, base_url):
    store = (StorePage(driver, base_url).open_authenticated().add_product(3)
             .checkout("Hugo Paulo", "hugo@example.com", "Purmerend, Netherlands"))
    assert store.order_reference() == "Reference: QC-2026-001"
