import time

from resources.automation_methods import AutomationMethods
from resources.page_object.base_page import BasePage
from resources.locators import Typo3Locators
from resources.validation_text_data import ValidationTextData as txt


class Typo3Page(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver)

        self.base_url = base_url
        staging_data = AutomationMethods().get_section_from_config(
            section_list=["Staging"]
        )

        url = f'{self.base_url}/{staging_data["typo3"]}'
        self.driver.get(url)

        self.enter_text(Typo3Locators.USERNAME_TYPO3, staging_data["user_name_typo3"])
        self.enter_text(Typo3Locators.PASSWORD_TYPO3, staging_data["password_typo3"])
        self.click_on_and_wait_for_a_new_page(Typo3Locators.LOGIN_BUTTON_TYPO3)
        while not self.page_is_loading():
            continue
        time.sleep(3)

        self.click_on(by_loctor=Typo3Locators.USERS_DIRECTORY)
