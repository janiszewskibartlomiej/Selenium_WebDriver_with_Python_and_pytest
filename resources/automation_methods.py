import os
import shutil
import smtplib
import sys
import time
import zipfile
from configparser import ConfigParser
from datetime import date, datetime, timedelta

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from pathlib import Path

import HtmlTestRunner
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys


class AutomationMethods:
    def __init__(self):
        self.config = ConfigParser()
        self.reports_path = self.get_path_from_dictionary_name(
            dictionary_name="reports"
        )

    # template of date example >> 20200715
    def current_date_str_from_number(self, sub_day=0) -> str:
        current_date = date.today()
        date_solution = current_date + timedelta(days=sub_day)
        current_date_template = str(date_solution).replace("-", "")
        return current_date_template

    def removing_directories_in_reports_by_number_of_day(self, n_day: int):
        list_remove_directory = []
        current_date_sub_days = int(self.current_date_str_from_number(sub_day=-n_day))

        entries = Path(self.reports_path)

        for entry in entries.iterdir():
            try:
                if int(entry.name) <= current_date_sub_days:
                    shutil.rmtree(f"{self.reports_path}/{entry.name}")
                    list_remove_directory.append(entry.name)
            except ValueError:
                continue
        message = f"\nRemoved directory: {list_remove_directory}\n"
        return message

    def html_test_runner_report(self) -> HtmlTestRunner:
        current_date_template = self.current_date_str_from_number()

        domain = self.get_section_from_config(section_list=["Staging"])["domain"]
        report_title = f"Test Results of {domain}"

        domain_strip = domain[:14]
        if domain_strip[-1] == "-":
            domain_strip = domain_strip[:13]

        file = sys.argv[0].split("_")
        browser = file[-1][:-3]

        output = "../reports/"

        if browser == "tests":
            browser = "all_browsers"
            report_title = report_title + " in Chrome & FireFox & IE"
            output = output[1:]

        report_name = f"{domain_strip}-{browser}"

        runner = HtmlTestRunner.HTMLTestRunner(
            output=output + current_date_template,
            combine_reports=True,
            report_title=report_title,
            report_name=report_name,
            verbosity=2,
            failfast=False,
            descriptions=True,
            buffer=False,
        )
        return runner

    def run_pytest_html_and_allure_report(self, by_name=None) -> list:
        allure_json_path = self.get_path_from_dictionary_name(
            dictionary_name="allure_json"
        )
        allure_html_reports_path = self.get_path_from_dictionary_name(
            dictionary_name="HTML_reports"
        )

        current_date = self.current_date_str_from_number()

        pytest_html_report_path = f"{self.reports_path}\\{current_date}\\pytest_hipp9-staging_report_{int(time.time())}.html"
        if by_name:
            flag_and_name = f"-k {by_name}"
        else:
            flag_and_name = ""
        os.system(
            f"pytest {flag_and_name} --html={pytest_html_report_path} --self-contained-html --alluredir {allure_json_path} -v"
        )
        os.chdir(allure_html_reports_path)
        os.system(f"allure generate {allure_json_path} --clean")
        allure_index_path = allure_html_reports_path + "\\allure-report"
        pytest_path = pytest_html_report_path.replace("\\", "/")
        allure_path = allure_index_path.replace("\\", "/")
        allure_zip = shutil.make_archive(
            base_name=allure_path, format="zip", root_dir=allure_html_reports_path
        )
        print(allure_zip.title(), " is DONE !")
        allure_zip_path = self.get_path_from_file_name(file_name="allure-report.zip")
        allure_zip_path = allure_zip_path.replace("\\", "/")
        return [pytest_path, allure_zip_path]

    @staticmethod
    def get_path_from_file_name(file_name: str) -> str:
        path = sys.path[1]
        if path[-3:] == "zip":
            path = sys.path[0]
        for root, dirs, files in os.walk(path):
            for file in files:
                if file == file_name:
                    abs_path = os.path.join(root, file)
                    return abs_path

    @staticmethod
    def get_path_from_dictionary_name(dictionary_name: str) -> str:
        path = sys.path[1]
        if path[-3:] == "zip":
            path = sys.path[0]
        for root, dirs, files in os.walk(path):
            for dictionary in dirs:
                if dictionary == dictionary_name:
                    abs_path = os.path.join(root, dictionary)
                    return abs_path

    def get_section_from_config(self, section_list: list) -> dict:
        path = self.get_path_from_file_name(file_name="config.cfg")
        self.config.read(path)
        data = dict()
        for item in section_list:
            section = self.config.items(item)
            data.update(section)
        return data

    def get_set_from_links_file(self, file_name: str) -> set:
        file_path = self.get_path_from_file_name(file_name)
        with open(file=file_path, mode="r", encoding="utf-8") as file:
            list_of_links = file.readlines()
            slice_links = set()
            for element in list_of_links:
                element = element[:-2]
                slice_links.add(element)
        return slice_links

    def get_driver(
        self,
        browser_name="chrome",
        headless=True,
        ie_del_cashe=False,
        firefox_del_cashe=False,
        chrome_del_cash=False,
    ):
        if browser_name == "chrome":
            chrome_options = webdriver.ChromeOptions()

            if headless:
                chrome_options.add_argument("--headless")

            chrome_path = self.get_path_from_file_name(file_name="chromedriver.exe")
            driver = webdriver.Chrome(
                executable_path=chrome_path, options=chrome_options
            )

            if chrome_del_cash:
                driver.get("chrome://settings/clearBrowserData")
                action = ActionChains(driver)
                time.sleep(2)
                action.send_keys(Keys.ENTER).perform()

            driver.set_page_load_timeout(30)
            driver.implicitly_wait(1)
            driver.maximize_window()
            return driver

        elif browser_name == "ie":
            if ie_del_cashe:
                caps = DesiredCapabilities.INTERNETEXPLORER
                caps["ignoreProtectedModeSettings"] = True
                caps["enableElementCacheCleanup"] = True
                caps["ie.ensureCleanSession"] = True
            else:
                caps = {}

            ie_path = AutomationMethods.get_path_from_file_name(
                file_name="IEDriverServer.exe"
            )
            driver = webdriver.Ie(executable_path=ie_path, capabilities=caps)
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(1)
            driver.maximize_window()
            return driver

        elif browser_name == "firefox":
            profile = webdriver.FirefoxProfile()
            profile.accept_untrusted_certs = True

            if firefox_del_cashe:
                profile.set_preference("browser.cache.disk.enable", False)
                profile.set_preference("browser.cache.memory.enable", False)
                profile.set_preference("browser.cache.offline.enable", False)
                profile.set_preference("network.http.use-cache", False)

            firefox_options = webdriver.FirefoxOptions()
            if headless:
                firefox_options.add_argument("--headless")

            firefox_path = AutomationMethods.get_path_from_file_name(
                file_name="geckodriver.exe"
            )
            driver = webdriver.Firefox(
                executable_path=firefox_path,
                firefox_profile=profile,
                options=firefox_options,
            )
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(1)
            driver.maximize_window()
            return driver

    def get_screenshot(
        self, name: str, driver: webdriver, dictionary_path: str
    ) -> None:
        original_size = driver.get_window_size()
        required_width = driver.execute_script(
            "return document.body.parentNode.scrollWidth"
        )
        required_height = driver.execute_script(
            "return document.body.parentNode.scrollHeight"
        )
        driver.set_window_size(required_width, required_height)

        if not os.path.exists(dictionary_path):
            os.makedirs(dictionary_path)

        t = time.localtime()
        current_time = time.strftime("%H-%M-%S", t)
        path = f"{dictionary_path}/screenshot_{name}_{current_time}.png"
        time.sleep(1)
        driver.get_screenshot_as_file(path)
        time.sleep(1)
        driver.set_window_size(original_size["width"], original_size["height"])

    def get_screenshot_documentation_from_links(
        self, set_of_links: set, domain: str, driver: webdriver, dictionary_path: str
    ) -> dict:
        driver = driver
        driver.set_page_load_timeout(30)
        incorrect_status_code = {}
        for link in set_of_links:
            response = requests.get(link)
            status = str(response.status_code)
            print("Link: ", link, "\t\t\t\t\tStatus code: ", status)
            driver.get(link)
            name = link.replace(str(domain), "").replace("/", "_")
            self.get_screenshot(
                name=name, driver=driver, dictionary_path=dictionary_path
            )
            if status[0] in ["4", "3", "5"]:
                incorrect_status_code[link] = status
        return incorrect_status_code

    def send_email(
        self,
        send_to=None,
        subject=None,
        message_conntent=None,
        files=None,
        use_tls=True,
    ):
        post = self.get_section_from_config(section_list=["Post"])

        if send_to is None:
            # send_to = post["receiver_email"]
            send_to = post["test"]
        else:
            send_to = send_to

        if subject is None:
            subject = post["subject"]
        else:
            subject = subject

        if message_conntent is None:
            message_conntent = """
            Cześć,\n 
            W załączeniu przesyłam raport z wynikami testów stworzonymi w pytest. \n
            Pozdro Bart
            """
        else:
            message_conntent = message_conntent

        if files is None:
            files = []

        sender_email = post["sender_email"]
        smtp_server = post["smtp_server"]
        port = 25
        password = post["password"]

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = send_to
        message["Subject"] = subject
        message["Date"] = formatdate(localtime=True)
        message["Cc"] = sender_email
        message.attach(MIMEText(message_conntent))

        if files:
            for path in files:
                with open(file=path, mode="rb") as file:
                    base_name = os.path.basename(path)
                    exe = path.split(".")[-1]
                    instance = MIMEApplication(
                        _data=file.read(), _subtype=exe, name=base_name
                    )
                    # instance = MIMEBase(_maintype="Application", _subtype=exe)
                    # instance.set_payload(file.read())
                    # encoders.encode_base64(instance)
                    instance.add_header(
                        _name="Content-Disposition",
                        _value="attachment",
                        filename=base_name,
                    )
                    message.attach(instance)

        with smtplib.SMTP(host=smtp_server, port=port) as server:
            server.ehlo_or_helo_if_needed()
            if use_tls:
                server.starttls()
                server.ehlo_or_helo_if_needed()
            server.login(user=sender_email, password=password)
            server.send_message(message)

    def get_date_from_delta_n_day(self, add_days: int) -> dict:
        today = datetime.today()
        future_date = today + timedelta(days=add_days)
        date_slice = datetime.strftime(future_date, "%Y-%m-%d")
        date_dict = {
            "day": date_slice[-2:],
            "month": date_slice[5:7],
            "year": date_slice[:4],
        }
        return date_dict


if __name__ == "__main__":
    set_of_link = AutomationMethods().get_set_from_links_file(
        file_name="files/links.csv"
    )
    driver = AutomationMethods().get_driver(browser_name="ie")
    AutomationMethods().get_screenshot_documentation_from_links(
        set_of_links=set_of_link,
        domain="",
        driver=driver,
        dictionary_path="../reports/ie_screen_every_page",
    )
