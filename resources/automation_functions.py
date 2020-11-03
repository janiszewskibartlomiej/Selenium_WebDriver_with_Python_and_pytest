import os
import shutil
import smtplib
import sys
import time
from datetime import date, datetime, timedelta
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from pathlib import Path

import HtmlTestRunner
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from sty import fg
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import tests.resources.constants as const

load_dotenv()


# template of date example >> 20200715
def current_date_str_from_number(sub_day=0) -> str:
    current_date = date.today()
    date_solution = current_date + timedelta(days=sub_day)
    current_date_template = date_solution.strftime("%Y%m%d")
    return current_date_template


def removing_directories_in_reports_by_number_of_day(n_day: int) -> str:
    list_remove_directory = []
    current_date_sub_days = int(current_date_str_from_number(sub_day=-n_day))

    reports_path = get_path_from_directory_name(directory_name=const.REPORTS)
    entries = Path(reports_path)
    for entry in entries.iterdir():
        try:
            if int(entry.name) <= current_date_sub_days:
                shutil.rmtree(f"{reports_path}/{entry.name}")
                list_remove_directory.append(entry.name)
        except ValueError:
            continue
    message = f"\nRemoved directory: {list_remove_directory}\n"
    return message


def html_test_runner_report() -> HtmlTestRunner:
    current_date_template = current_date_str_from_number()

    domain = os.environ.get("DOMAIN")
    report_title = f"Test Results of {domain}"

    domain_strip = domain[:14]
    if domain_strip[-1] == "-":
        domain_strip = domain_strip[:13]

    file = sys.argv[0].split("_")
    browser = file[-1][:-3]

    output = "../reports/"

    if browser == const.TESTS:
        browser = "all_browsers"
        report_title = report_title + " in Chrome & FireFox "
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


def run_pytest_html_and_allure_report(by_name=None) -> list:
    allure_json_path = change_win_sep(path=get_path_from_directory_name(
        directory_name=const.ALLURE_JSON
    ))

    allure_html_reports_path = change_win_sep(path=get_path_from_directory_name(
        directory_name=const.HTML_REPORTS
    ))

    reports_path = change_win_sep(path=get_path_from_directory_name(directory_name=const.REPORTS))

    current_date = current_date_str_from_number()

    pytest_html_report_path = \
        f"{reports_path}{os.sep}{current_date}{os.sep}pytest_hipp9-staging_report_{int(time.time())}.html"

    flag_and_name = f"-k {by_name}" if by_name else ""

    os.system(
        f"pytest -v {flag_and_name} --html={pytest_html_report_path} --self-contained-html --alluredir {allure_json_path} -n=4"
    )
    os.chdir(allure_html_reports_path)
    os.system(f"allure generate {allure_json_path} --clean")
    allure_index_path = change_win_sep(path=f"{allure_html_reports_path}{os.sep}allure-report")
    allure_zip = shutil.make_archive(
        base_name=allure_index_path, format="zip", root_dir=allure_html_reports_path
    )
    print(allure_zip.title(), " is DONE !")
    allure_zip_path = change_win_sep(path=get_path_from_file_name(file_name="allure-report.zip"))
    return [pytest_html_report_path, allure_zip_path]


def get_path_from_file_name(file_name: str) -> str:
    path = sys.path[1]
    if Path(path).suffix == const.ZIP_EXTENSION:
        path = sys.path[0]
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == file_name:
                abs_path = os.path.join(root, file)
                return abs_path


def get_path_from_directory_name(directory_name: str) -> str:
    path = sys.path[1]
    if Path(path).suffix == const.ZIP_EXTENSION:
        path = sys.path[0]
    for root, dirs, files in os.walk(path):
        for dictionary in dirs:
            if dictionary == directory_name:
                abs_path = os.path.join(root, dictionary)
                return abs_path


def get_set_from_links_file(file_name: str) -> set:
    file_path = get_path_from_file_name(file_name)
    with open(file=file_path, mode="r", encoding="utf-8") as file:
        list_of_links = file.readlines()
        slice_links = set()
        for element in list_of_links:
            element = element[:-2]
            slice_links.add(element)
    return slice_links


def get_driver(
        browser_name="chrome",
        headless=True,
        firefox_del_cashe=False,
        chrome_del_cash=False
):
    if browser_name == "chrome":
        chrome_options = webdriver.ChromeOptions()

        if headless:
            chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(), options=chrome_options
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

        driver = webdriver.Firefox(
            executable_path=GeckoDriverManager().install(),
            firefox_profile=profile,
            options=firefox_options,
        )
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(1)
        driver.maximize_window()
        return driver


def get_screenshot(
        name: str, driver: webdriver, directory_path: str
) -> None:
    original_size = driver.get_window_size()
    required_width = driver.execute_script(
        "return document.body.parentNode.scrollWidth"
    )
    required_height = driver.execute_script(
        "return document.body.parentNode.scrollHeight"
    )
    driver.set_window_size(required_width, required_height)

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    t = time.localtime()
    current_time = time.strftime("%H-%M-%S", t)
    path = f"{directory_path}/screenshot_{name}_{current_time}.png"
    time.sleep(1)
    driver.get_screenshot_as_file(path)
    time.sleep(1)
    driver.set_window_size(original_size["width"], original_size["height"])


def get_list_of_path_to_attachment(
        has_attachment, attachment_names, list_of_path_to_files=None
) -> list:
    if list_of_path_to_files is None:
        list_of_path_to_files = []

    if has_attachment:
        if "," in attachment_names:
            list_attachment_names = attachment_names.split(",")
            for name in list_attachment_names:
                attachment_path = get_path_from_file_name(name)
                list_of_path_to_files.append(attachment_path)

        else:
            attachment_path = get_path_from_file_name(
                file_name=attachment_names
            )
            list_of_path_to_files.append(attachment_path)

    return list_of_path_to_files


def get_screenshot_documentation_from_links(
        set_of_links: set, domain: str, driver: webdriver, dictionary_path: str
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
        get_screenshot(
            name=name, driver=driver, directory_path=dictionary_path
        )
        if status[0] in ["4", "3", "5"]:
            incorrect_status_code[link] = status
    return incorrect_status_code


def print_message_in_color(message: str, rgb_color: str) -> None:
    list_of_volume = rgb_color.split(",")
    response = (
            fg(list_of_volume[0], list_of_volume[1], list_of_volume[2])
            + "\n\n"
            + message
            + "\n"
            + fg.rs
    )
    print(response)


def send_email(
        send_to=None,
        subject=None,
        message_content=None,
        files=None,
        use_tls=True,
):
    send_to = send_to if send_to else os.environ.get("ADMIN_EMAIL")

    subject = subject if subject else os.environ.get("SUBJECT")

    message_content = message_content if message_content else const.MESSAGE

    if not files:
        files = []

    sender_email = os.environ.get("SENDER_EMAIL")
    smtp_server = os.environ.get("SMTP_SERVER")
    port = int(os.environ.get("PORT"))
    password = os.environ.get("EMAIL_PASSWORD")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = send_to
    message["Subject"] = subject
    message["Date"] = formatdate(localtime=True)
    message["Cc"] = sender_email
    message.attach(MIMEText(message_content))

    if files:
        set_attachments(files_path=files, message=message)

    with smtplib.SMTP(host=smtp_server, port=port) as server:
        server.ehlo_or_helo_if_needed()
        if use_tls:
            server.starttls()
            server.ehlo_or_helo_if_needed()
        server.login(user=sender_email, password=password)
        server.send_message(message)

    print_message_in_color(message=f"Send successful email, subject = {subject}",
                           rgb_color="255,10,10")


def get_date_from_delta_n_day(add_days: int) -> dict:
    today = datetime.today()
    future_date = today + timedelta(days=add_days)
    date_dict = {
        "day": future_date.day,
        "month": future_date.month,
        "year": future_date.year,
    }
    return date_dict


def make_directory(location_by_directory_name: str, creating_of_directory_name: str) -> str:
    location_path = get_path_from_directory_name(directory_name=location_by_directory_name)
    os.makedirs(location_path + os.sep + creating_of_directory_name)
    dictionary_path = get_path_from_directory_name(directory_name=creating_of_directory_name)
    return dictionary_path


def change_win_sep(path: str) -> str:
    change_path = path.replace("\\", "/")
    return change_path


def set_attachments(files_path: list, message: MIMEMultipart) -> None:
    for path in files_path:
        with open(file=path, mode="rb") as file:
            base_name = os.path.basename(path)
            exe = path.split(".")[-1]
            instance = MIMEApplication(
                _data=file.read(), _subtype=exe, name=base_name
            )
        instance.add_header(
            _name="Content-Disposition",
            _value="attachment",
            filename=base_name,
        )
        message.attach(instance)
