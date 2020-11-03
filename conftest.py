import os
import sys
import time
from configparser import ConfigParser
from datetime import datetime

from py.xml import html
import pytest

from selenium import webdriver
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

render_collapsed = True

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)


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
                f'Domain: {os.environ.get("DOMAIN")}'
            )
        ]
    )


@pytest.fixture(params=["hipp", "dlalekarzy"])
def base_url(request):
    base_url = None

    if request.param == "hipp":
        base_url = os.environ.get("ACCESS")

    if request.param == "dlalekarzy":
        base_url = os.environ.get("ACCESS_DOCTOR_PAGE")

    yield base_url
    pass


@pytest.fixture(params=["chrome", "firefox"])
def driver(
        request,
        chrome_del_cache=False,
        chrome_headless=True,
        firefox_del_cache=False,
        firefox_headless=True,
):
    driver = None
    if request.param == "chrome":
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })

        if chrome_headless:
            chrome_options.headless = True

        driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(), options=chrome_options
        )

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
            firefox_options.headless = True

        driver = webdriver.Firefox(
            executable_path=GeckoDriverManager().install(),
            firefox_profile=profile,
            options=firefox_options,
        )

    driver.set_page_load_timeout(30)
    driver.implicitly_wait(1)
    driver.delete_all_cookies()
    driver.maximize_window()
    yield driver
    driver.quit()
