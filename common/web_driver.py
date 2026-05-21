# common/web_driver.py
from playwright.sync_api import sync_playwright

def get_page(headless=False):
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless)
    page = browser.new_page()
    return page, browser