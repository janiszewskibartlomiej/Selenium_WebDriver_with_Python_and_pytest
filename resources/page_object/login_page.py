import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from ..locators import LoginPageLocators


class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        url = f'{self.base_url}//klub/zaloguj-sie'
        self.driver.get(url)

    def login_as(self, username: str, password: str, submit=True):

        self.enter_text(LoginPageLocators.USERNAME_FIELD, username)
        if submit == False:
            self.enter_text_and_click_enter_and_wait_for_a_new_page(LoginPageLocators.PASSWORD_FIELD, password)
        else:
            self.enter_text(LoginPageLocators.PASSWORD_FIELD, password)
            self.click_on_and_wait_for_a_new_page(LoginPageLocators.SUBMIT_BTN)
        time.sleep(3)

    def incorrect_login_as(self, username: str, password: str, submit=True):
        self.enter_text(LoginPageLocators.USERNAME_FIELD, username)
        if submit == False:
            self.enter_text_and_click_enter(LoginPageLocators.PASSWORD_FIELD, password)
        else:
            self.enter_text(LoginPageLocators.PASSWORD_FIELD, password)
            self.click_on(LoginPageLocators.SUBMIT_BTN)
        while not self.page_is_loading():
            continue
        time.sleep(3)
