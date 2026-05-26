import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True 可不显示浏览器
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()

def test_login_success(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    assert page.url == "https://www.saucedemo.com/inventory.html"

def test_login_failed(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("locked_out_user", "secret_sauce")
    error = login_page.get_error_message()
    assert "Sorry, this user has been locked out" in error