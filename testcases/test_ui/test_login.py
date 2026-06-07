# testcases/test_ui/test_login.py
import os
import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from common.loader import load_yaml

# ==================== fixture ====================

@pytest.fixture(scope="function")
def page():
    headless = os.getenv("CI", "false").lower() == "true"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()

# ==================== 数据驱动登录用例 ====================

login_data = load_yaml("login_data.yaml")

@pytest.mark.parametrize("data", login_data, ids=[d["test_name"] for d in login_data])
def test_login_data_driven(page, data):
    """数据驱动登录测试：正常/锁定/空用户名"""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(data["username"], data["password"])

    if "expected_url" in data:
        login_page.assert_url_contains(data["expected_url"])
        login_page.take_screenshot(f"login_{data['test_name']}")
    elif "expected_error" in data:
        error = login_page.get_error_message()
        assert data["expected_error"] in error
        login_page.take_screenshot(f"login_{data['test_name']}")

# ==================== 原有手动用例（保留） ====================

def test_login_success(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    login_page.assert_url_contains("inventory.html")
    login_page.take_screenshot("login_success")

def test_login_failed(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("locked_out_user", "secret_sauce")
    error = login_page.get_error_message()
    assert "Sorry, this user has been locked out" in error
    login_page.take_screenshot("login_failed")

def test_login_no_username(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("", "secret_sauce")
    error = login_page.get_error_message()
    assert "Username is required" in error
    login_page.take_screenshot("login_no_username")

# ==================== 业务流程用例 ====================

def test_sort_products_and_select_first(page):
    """TC04: 按价格排序后选择第一个商品"""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    inventory.sort_by_price_low_to_high()
    item_name = inventory.get_first_item_name()
    inventory.click_first_item_name()
    assert item_name in page.url or page.locator(".inventory_details_name").text_content() == item_name

def test_add_item_to_cart(page):
    """TC05: 加入购物车验证"""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    inventory.add_first_item_to_cart()
    count = inventory.get_cart_count()
    assert count == "1"

    inventory.go_to_cart()
    cart = CartPage(page)
    assert cart.get_item_count() == 1

def test_complete_checkout(page):
    """TC06: 完整下单流程"""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    inventory.add_first_item_to_cart()
    inventory.go_to_cart()

    cart = CartPage(page)
    cart.proceed_to_checkout()

    checkout = CheckoutPage(page)
    checkout.fill_shipping_info("Test", "User", "12345")
    checkout.finish_order()

    confirmation = checkout.get_confirmation_message()
    assert "THANK YOU" in confirmation.upper()