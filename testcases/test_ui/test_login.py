# testcases/test_ui/test_login.py
import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage


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