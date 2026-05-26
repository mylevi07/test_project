# common/web_base.py
import os
from datetime import datetime
from playwright.sync_api import Page, expect


class WebBase:
    """Web 自动化通用操作封装"""

    def __init__(self, page: Page):
        self.page = page
        self.screenshot_dir = "screenshots"

        # 确保截图目录存在
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

    def wait_for_element(self, selector: str, timeout: int = 10000):
        """等待元素可见"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    def click(self, selector: str):
        """点击元素（带等待）"""
        self.wait_for_element(selector)
        self.page.click(selector)

    def fill(self, selector: str, text: str):
        """输入文本（带等待+清空）"""
        self.wait_for_element(selector)
        self.page.fill(selector, text)

    def get_text(self, selector: str) -> str:
        """获取元素文本"""
        self.wait_for_element(selector)
        return self.page.text_content(selector)

    def scroll_to(self, selector: str):
        """滚动到指定元素"""
        self.page.locator(selector).scroll_into_view_if_needed()

    def take_screenshot(self, name: str = None):
        """截图并保存到 screenshots 目录"""
        if name is None:
            name = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.screenshot_dir, f"{name}.png")
        self.page.screenshot(path=filepath)
        return filepath

    def assert_url_contains(self, expected: str):
        """断言当前 URL 包含指定字符串"""
        current_url = self.page.url
        assert expected in current_url, f"URL 不包含 '{expected}'，当前 URL: {current_url}"
        
    def assert_text_visible(self, text: str):
        """断言页面上包含指定文本"""
        expect(self.page.locator(f"text={text}")).to_be_visible()