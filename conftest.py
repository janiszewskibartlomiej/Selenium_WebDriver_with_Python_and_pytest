import time
from configparser import ConfigParser
from datetime import datetime

from py.xml import html
import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from resources.automation_methods import AutomationMethods

render_collapsed = True


def pytest_html_results_table_header(cells):
    cells.insert(1, html.th("Time", class_="sortable time", col="time"))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(datetime.now(), class_="col-time"))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)


def pytest_html_report_title(report):
    report.title = "pytest Hipp9 report on staging"


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend(
        [
            html.p(
                f'Domain: {AutomationMethods().get_section_from_config(section_list=["Staging"])["domain"]}'
            )
        ]
    )


@pytest.fixture(name="test_data_from_fixture")
def test_data():
    config = ConfigParser()
    config_path = AutomationMethods().get_path_from_file_name(file_name="config.cfg")
    config.read(config_path)
    data = dict()
    common_data = config.items("Common_data")
    data.update(dict(common_data))
    staging_data = config.items("Staging")
    data.update(dict(staging_data))
    return data


@pytest.fixture(params=["chrome", "firefox", "ie"])
def driver(
    request,
    chrome_del_cache=False,
    chrome_headless=False,
    firefox_del_cache=False,
    firefox_headless=False,
    ie_del_cache=True,
):
    # global driver
    if request.param == "chrome":
        chrome_path = AutomationMethods().get_path_from_file_name("chromedriver.exe")
        # chrome_path = "drivers/chromedriver.exe"
        chrome_options = webdriver.ChromeOptions()
        if chrome_headless:
            chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

        if chrome_del_cache:
            driver.get("chrome://settings/clearBrowserData")
            action = ActionChains(driver)
            time.sleep(2)
            action.send_keys(Keys.ENTER).perform()

    if request.param == "firefox":
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True

        if firefox_del_cache:
            profile.set_preference("browser.cache.disk.enable", False)
            profile.set_preference("browser.cache.memory.enable", False)
            profile.set_preference("browser.cache.offline.enable", False)
            profile.set_preference("network.http.use-cache", False)

        firefox_options = webdriver.FirefoxOptions()

        if firefox_headless:
            firefox_options.add_argument("--headless")

        firefox_path = AutomationMethods().get_path_from_file_name(
            file_name="geckodriver.exe"
        )
        # firefox_path = "drivers/geckodriver.exe"

        driver = webdriver.Firefox(
            executable_path=firefox_path,
            firefox_profile=profile,
            options=firefox_options,
        )

    if request.param == "ie":
        if ie_del_cache:
            caps = DesiredCapabilities.INTERNETEXPLORER
            caps["ignoreProtectedModeSettings"] = True
            caps["enableElementCacheCleanup"] = True
            caps["ie.ensureCleanSession"] = True
        else:
            caps = {}

        ie_path = AutomationMethods().get_path_from_file_name(
            file_name="IEDriverServer.exe"
        )
        # ie_path = "drivers/IEDriverServer.exe"

        driver = webdriver.Ie(executable_path=ie_path, capabilities=caps)

    driver.set_page_load_timeout(30)
    driver.implicitly_wait(1)
    driver.maximize_window()
    yield driver
    driver.quit()
