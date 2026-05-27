#商品列表页面
from playwright.sync_api import Page
from common.web_base import WebBase

class InventoryPage(WebBase):
    def __init__(self, page: Page):
        super().__init__(page)
        # 排序下拉框
        self.sort_dropdown = ".product_sort_container"
        # 商品名称（取第一个）
        self.first_item_name = ".inventory_item_name"
        # 第一个商品的“加入购物车”按钮
        self.first_add_to_cart_btn = "button.btn_inventory"
        # 购物车图标和徽章
        self.cart_icon = ".shopping_cart_link"
        self.cart_badge = ".shopping_cart_badge"

    def sort_by_price_low_to_high(self):
        """按价格从低到高排序"""
        self.page.select_option(self.sort_dropdown, "lohi")

    def get_first_item_name(self):
        return self.get_text(self.first_item_name)

    def click_first_item_name(self):
        """点击第一个商品名称，进入详情页"""
        self.click(self.first_item_name)

    def add_first_item_to_cart(self):
        """在列表页直接将第一个商品加入购物车"""
        self.click(self.first_add_to_cart_btn)

    def go_to_cart(self):
        self.click(self.cart_icon)

    def get_cart_count(self):
        """获取购物车徽章数量"""
        if self.page.locator(self.cart_badge).is_visible():
            return self.get_text(self.cart_badge)
        return "0"
    