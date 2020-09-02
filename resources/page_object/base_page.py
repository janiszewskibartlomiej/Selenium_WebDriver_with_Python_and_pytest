import os
import random
import time
from datetime import date, datetime, timedelta

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.color import Color
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

from resources.automation_methods import AutomationMethods


class BasePage:
    """
    Base Page class that hold common elements
    and functionalities to all pages in app
    """

    def __init__(self, driver):
        self.driver = driver
        # self.base_url = AutomationMethods().get_section_from_config(section_list=["Staging"])["access"]
        self.base_url = AutomationMethods().get_section_from_config(section_list=["Staging"])["access_doctor_page"]

    def get_user_name(self):
        staging_data = AutomationMethods().get_section_from_config(section_list=["Staging"])

        if self.base_url == staging_data["access"]:
            user_name = staging_data["user_name"]

        elif self.base_url == staging_data["access_doctor_page"]:
            user_name = staging_data["user_name_doctor_page"]

        return user_name

    def click_on_and_wait_for_a_new_page(self, by_loctor: tuple):
        old_page = self.driver.find_element_by_tag_name('html')
        web_element = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable(by_loctor))
        web_element.click()
        # new_page = self.driver.find_element_by_tag_name('html')
        WebDriverWait(self.driver, 100).until(EC.staleness_of(old_page))
        time.sleep(1)

    def click_on(self, by_loctor: tuple):
        web_element = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable(by_loctor))
        web_element.click()
        while not self.page_is_loading():
            continue
        time.sleep(1)

    def assert_element_text(self, by_locator: tuple, element_text: str):
        web_element = WebDriverWait(self.driver, 100).until(EC.text_to_be_present_in_element(by_locator, element_text))
        assert web_element is True

    def assert_element_text_in_page_source(self, element_text: str):
        while not self.page_is_loading():
            continue
        page_source = self.driver.page_source
        assert element_text in page_source

    def assert_element_color_hex(self, by_locator: tuple, color_hex: str):
        web_element = WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located(by_locator))
        color_element = Color.from_string(web_element.value_of_css_property('color'))
        assert color_element.hex == color_hex

    def assert_path_in_current_url(self, path: str):
        assert_path_in_url = WebDriverWait(self.driver, 100).until(EC.url_contains(url=path))
        assert assert_path_in_url is True

    def enter_text(self, by_locator: tuple, text: str):
        element = WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located(by_locator))
        element.clear()
        element.send_keys(text)

    def enter_text_and_click_enter(self, by_locators: tuple, text: str):
        element = WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located(by_locators))
        element.clear()
        element.send_keys(text + Keys.ENTER)

    def enter_text_and_click_enter_and_wait_for_a_new_page(self, by_locators: tuple, text: str):
        old_page = self.driver.find_element_by_tag_name('html')
        element = WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located(by_locators))
        element.clear()
        element.send_keys(text + Keys.ENTER)
        WebDriverWait(self.driver, 100).until(staleness_of(old_page))

    def page_is_loading(self):
        page_status = self.driver.execute_script("return document.readyState")
        if page_status == "complete":
            return True
        else:
            yield False

    def is_clickable(self, by_locator: tuple) -> bool:
        element = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable(by_locator))
        return bool(element)

    def element_is_visible(self, by_locator: tuple) -> bool:
        element = WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located(by_locator))
        return bool(element)

    def element_is_not_visible(self, by_locator: tuple) -> bool:
        element = WebDriverWait(self.driver, 100).until(EC.invisibility_of_element_located(by_locator))
        return bool(element)

    def get_element(self, by_locator: tuple):
        element = WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located(by_locator))
        return element

    def hover_to(self, by_locator: tuple) -> ActionChains:
        element = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable(by_locator))
        return ActionChains(self.driver).move_to_element(element).perform()

    def choose(self, drop_down_select: tuple, name: str):
        drop_down = WebDriverWait(self, 100).until(EC.visibility_of_element_located(drop_down_select))
        drop_down.find_element(By.NAME(name)).click()

    def quit(self):
        self.driver.close()
        self.driver.quit()

    def visit_page(self, endpoit: str):
        url = self.base_url + endpoit
        return self.driver.get(url)

    def open_new_tab_and_switch(self):
        tab = self.driver.execute_script("window.open('');")
        return self.driver.switch_to.window(tab[1])

    def get_current_url(self):
        return self.driver.current_url

    def get_random_firstname_from_csv(self, path: str) -> str:
        # ROOT_DIR = os.path.abspath(os.curdir)
        with open(file=str(path), encoding="utf8", mode="r") as file:
            first_name = file.read().splitlines()
            random_name = random.choice(first_name)
            return random_name

    def get_random_town_name_from_csv(self, path: str) -> str:
        with open(file=str(path), encoding="utf8", mode="r") as file:
            town_list = file.read().splitlines()
            random_town_data = random.choice(town_list)
            random_town_name = random_town_data.split(";")
            return random_town_name[1]

    def get_random_street_name_from_csv(self, path: str) -> str:
        with open(file=str(path), encoding="utf8", mode="r") as file:
            street_list = file.read().splitlines()
            random_street_data = random.choice(street_list)
            random_street_name = random_street_data.split(";")
            return random_street_name[7]



    def get_random_post_code_and_town_name_from_csv(self, path: str) -> dict:
        with open(file=str(path), encoding="utf8", mode="r") as file:
            data_list = file.read().splitlines()
            random_data = random.choice(data_list)
            random_data_split = random_data.split(";")
            post_code = random_data_split[0]
            street_name = random_data_split[1]
            town_name = random_data_split[2]
            address_dict = {
                "post_code": post_code,
                "town_name": town_name
            }
            return address_dict

    def get_random_number(self, today=False) -> str:
        if today:
            current_day = date.today()
            str_number = (str(current_day))[-2:]
        else:
            random_number = random.randint(1, 29)
            str_number = str(random_number)
            if len(str_number) < 2:
                str_number = "0" + str_number
        return str_number

    def get_random_street_number(self) -> str:
        random_number = random.randint(1, 1000)
        char_list = ["", "", "B", "", "A", "", ""]
        random_char = random.choice(char_list)
        return str(random_number) + random_char

    def get_random_phone_number(self) -> str:
        sequence_list = random.sample(range(100, 999), 3)
        return f"{sequence_list[0]} {sequence_list[1]} {sequence_list[2]}"

    def get_month_number(self, add_number=0) -> str:
        month_number = date.today().month + add_number
        str_next_month = str(month_number)
        if len(str_next_month) < 2:
            str_next_month = "0" + str_next_month
        return str_next_month

    def do_screenshot(self, name: str) -> None:
        while not self.page_is_loading():
            continue
        original_size = self.driver.get_window_size()
        required_width = self.driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
        self.driver.set_window_size(required_width, required_height)

        current_date = date.today()
        current_date_template = str(current_date).replace("-", "")
        reports_path = AutomationMethods().get_path_from_dictionary_name(dictionary_name="reports")
        reports_path = reports_path.replace("\\", "/")
        if not os.path.exists(f"{reports_path}/{current_date_template}"):
            os.makedirs(f"{reports_path}/{current_date_template}")

        t = time.localtime()
        current_time = time.strftime("%H-%M-%S", t)
        path = f"{reports_path}/{current_date_template}/screenshot_{name}_{current_time}.png"
        self.driver.get_screenshot_as_file(path)
        self.driver.set_window_size(original_size['width'], original_size['height'])

