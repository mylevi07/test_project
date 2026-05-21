import pytest
from common.web_driver import get_page
from common.api_client import load_config

config = load_config()
url = config["sauce_demo"]["url"]
user = config["sauce_demo"]["credentials"]["standard_user"]["username"]
pwd = config["sauce_demo"]["credentials"]["standard_user"]["password"]

def test_login():
    page, browser = get_page()
    page.goto(url)
    page.fill("#user-name", user)
    page.fill("#password", pwd)
    page.click("#login-button")
    assert "inventory.html" in page.url
    browser.close()