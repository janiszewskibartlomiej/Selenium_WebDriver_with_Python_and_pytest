import os
import time

from dotenv import load_dotenv

import resources.constants as const
from resources.locators import Typo3Locators
from resources.page_object.base_page import BasePage

load_dotenv()


class Typo3Page(BasePage):

    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.driver = driver
        self.base_url = base_url

        url = f'{self.base_url}/{const.TYPO3}'
        self.driver.get(url)

        self.enter_text(Typo3Locators.USERNAME_TYPO3, os.environ.get("USER_NAME_TYPO3"))
        self.enter_text(Typo3Locators.PASSWORD_TYPO3, os.environ.get("PASSWORD_TYPO3"))
        self.click_on_and_wait_for_a_new_page(Typo3Locators.LOGIN_BUTTON_TYPO3)
        while not self.page_is_loading():
            continue
        time.sleep(3)

        self.click_on(by_loctor=Typo3Locators.USERS_DIRECTORY)
