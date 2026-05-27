from playwright.sync_api import Page
from common.web_base import WebBase

class CartPage(WebBase):
    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_item = ".cart_item"
        self.checkout_button = "#checkout"

    def get_item_count(self):
        """购物车中商品数量"""
        return self.page.locator(self.cart_item).count()

    def proceed_to_checkout(self):
        self.click(self.checkout_button)