# testcases/test_ui/test_login.py
import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


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
    """TC03: 不输入用户名直接登录"""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("", "secret_sauce")
    error = login_page.get_error_message()
    assert "Username is required" in error
    login_page.take_screenshot("login_no_username")

def test_sort_products_and_select_first(page):
    """TC04: 按价格排序后选择第一个商品，验证商品名称"""
    # 先登录
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    # 商品页操作
    inventory = InventoryPage(page)
    inventory.sort_by_price_low_to_high()
    item_name = inventory.get_first_item_name()
    inventory.click_first_item_name()

    # 验证详情页标题与选中的商品名一致
    assert item_name in page.url or page.locator(".inventory_details_name").text_content() == item_name


def test_add_item_to_cart(page):
    """TC05: 将商品加入购物车，验证购物车徽章数字"""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    # 直接添加第一个商品
    inventory.add_first_item_to_cart()
    count = inventory.get_cart_count()
    assert count == "1", f"Expected cart count 1, but got {count}"

    # 进入购物车页再次验证
    inventory.go_to_cart()
    cart = CartPage(page)
    assert cart.get_item_count() == 1


def test_complete_checkout(page):
    """TC06: 完整下单流程，验证成功提示"""
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