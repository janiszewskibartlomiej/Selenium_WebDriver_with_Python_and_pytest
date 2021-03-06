import os
import time

from dotenv import load_dotenv
from resources.page_object.base_page import BasePage
from resources.locators import LoginPageLocators
import resources.constants as const

load_dotenv()


class LoginPage(BasePage):

    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.driver = driver
        self.base_url = base_url

        if self.base_url == os.environ.get("ACCESS"):
            self.endpoint = const.LOGIN_ENDPOINT
        elif self.base_url == os.environ.get("ACCESS_DOCTOR_PAGE"):
            self.endpoint = const.LOGIN_ENDPOINT_DOCTOR_PAGE

        url = f"{self.base_url}{self.endpoint}"
        self.driver.get(url)

    def login_as(
            self,
            username,
            password,
            enter_key=False
    ):
        self.enter_text(
            LoginPageLocators.USERNAME_FIELD,
            username
        )
        if enter_key:
            self.enter_text_and_click_enter_and_wait_for_a_new_page(
                LoginPageLocators.PASSWORD_FIELD,
                password
            )
        else:
            self.enter_text(
                LoginPageLocators.PASSWORD_FIELD,
                password
            )
            self.click_on_and_wait_for_a_new_page(LoginPageLocators.SUBMIT_BUTTON)
        while not self.page_is_loading():
            continue
        time.sleep(3)

    def incorrect_login_as(
            self,
            username,
            password,
            enter_key=False
    ):
        self.enter_text(
            LoginPageLocators.USERNAME_FIELD,
            username
        )
        if enter_key:
            self.enter_text_and_click_enter(
                LoginPageLocators.PASSWORD_FIELD,
                password
            )
        else:
            self.enter_text(
                LoginPageLocators.PASSWORD_FIELD,
                password
            )
            self.click_on(LoginPageLocators.SUBMIT_BUTTON)
        while not self.page_is_loading():
            continue
        time.sleep(3)
