from playwright.sync_api import Page
from common.web_base import WebBase

class CheckoutPage(WebBase):
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = "#first-name"
        self.last_name_input = "#last-name"
        self.postal_code_input = "#postal-code"
        self.continue_button = "#continue"
        self.finish_button = "#finish"
        self.complete_header = ".complete-header"

    def fill_shipping_info(self, first: str, last: str, zip_code: str):
        self.fill(self.first_name_input, first)
        self.fill(self.last_name_input, last)
        self.fill(self.postal_code_input, zip_code)
        self.click(self.continue_button)

    def finish_order(self):
        self.click(self.finish_button)

    def get_confirmation_message(self):
        return self.get_text(self.complete_header)