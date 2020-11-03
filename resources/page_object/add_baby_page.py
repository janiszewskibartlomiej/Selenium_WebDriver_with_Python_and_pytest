import os

from selenium.webdriver.support.select import Select

import resources.constants as const
from resources.locators import AddBabyLocators
from resources.page_object.base_page import BasePage
from resources.page_object.login_page import LoginPage
from resources.automation_functions import removing_directories_in_reports_by_number_of_day

removing_directories_in_reports_by_number_of_day(
    n_day=int(os.environ.get("REMOVING_REPORTS_BY_NUMBER_OF_DAY"))
)


class AddBabyPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.base_url = os.environ.get("ACCESS")

        LoginPage(self.driver, self.base_url).login_as(
            username=os.environ.get("USER_EMAIL"), password=os.environ.get("PASSWORD")
        )
        url = f"{self.base_url}/{const.ADD_BABY_ENDPOINT}"
        self.driver.get(url)

    def select_date(self, day: str, month: str, year: str, pregnant=True):
        if pregnant:
            day_locator = AddBabyLocators.PREGNANT_DAY
            month_locator = AddBabyLocators.PREGNANT_MONTH
            year_locator = AddBabyLocators.PREGNANT_YEAR
        else:
            day_locator = AddBabyLocators.BORN_DAY
            month_locator = AddBabyLocators.BORN_MONTH
            year_locator = AddBabyLocators.BORN_YEAR

        month_select = Select(
            self.get_element(by_locator=month_locator)
        )
        list_of_month = [i.text for i in month_select.options]
        index = int(month)
        month_select.select_by_visible_text(list_of_month[index])

        day_select = Select(
            self.get_element(by_locator=day_locator)
        )
        day_select.select_by_visible_text(str(day))

        year_select = Select(
            self.get_element(by_locator=year_locator)
        )
        year_select.select_by_visible_text(str(year))
