from selenium.webdriver.support.select import Select

from resources.page_object.base_page import BasePage
from resources.page_object.login_page import LoginPage
from resources.automation_methods import AutomationMethods
from resources.locators import AddBabyLocators
from resources.validation_text_data import ValidationTextData as txt


class AddBabyPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.base_url = AutomationMethods().get_section_from_config(
            section_list=["Staging"]
        )["access"]

        common_data = AutomationMethods().get_section_from_config(
            section_list=["Common_data"]
        )
        LoginPage(self.driver, self.base_url).login_as(
            username=common_data["user_email"], password=common_data["password"]
        )
        url = f"{self.base_url}/{txt.ADD_BABY_ENDPOINT}"
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

        month_select = Select(self.get_element(by_locator=month_locator))
        list_of_month = [i.text for i in month_select.options]
        index = int(month)
        month_select.select_by_visible_text(list_of_month[index])

        day_select = Select(self.get_element(by_locator=day_locator))
        day_select.select_by_visible_text(str(day))

        year_select = Select(self.get_element(by_locator=year_locator))
        year_select.select_by_visible_text(str(year))
