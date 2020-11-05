import os
import time

import pytest

import resources.constants as const
from resources.automation_functions import (
    removing_directories_in_reports_by_number_of_day,
)
from resources.locators import LoginPageLocators, ForDoctorsPage
from resources.page_object.login_page import LoginPage

removing_directories_in_reports_by_number_of_day(
    n_day=int(os.getenv(key="REMOVING_REPORTS_BY_NUMBER_OF_DAY", default="7"))
)


@pytest.mark.captcha
@pytest.mark.parametrize(
    "user_first, password_first, "
    "user_second, password_second, "
    "user_third, password_third, "
    "enter_key, one_correct_login",
    [
        (  # captcha is visible after three times incorrect login
            os.environ.get("INCORRECT_EMAIL_1"),
            os.environ.get("INCORRECT_PASSWORD_1"),
            os.environ.get("INCORRECT_EMAIL_2"),
            os.environ.get("INCORRECT_PASSWORD_2"),
            os.environ.get("INCORRECT_EMAIL_3"),
            os.environ.get("INCORRECT_PASSWORD_3"),
            False,
            False,
        ),
        (  # captcha is visible after three times incorrect login - use enter key
            os.environ.get("INCORRECT_EMAIL_1"),
            os.environ.get("INCORRECT_PASSWORD_1"),
            os.environ.get("INCORRECT_EMAIL_2"),
            os.environ.get("INCORRECT_PASSWORD_2"),
            os.environ.get("INCORRECT_EMAIL_3"),
            os.environ.get("INCORRECT_PASSWORD_3"),
            True,
            False,
        ),
        (  # captcha is visible after three times incorrect login total quantity
            os.environ.get("INCORRECT_EMAIL_4"),
            os.environ.get("INCORRECT_PASSWORD_4"),
            os.environ.get("INCORRECT_EMAIL_1"),
            os.environ.get("INCORRECT_PASSWORD_2"),
            os.environ.get("INCORRECT_EMAIL_3"),
            os.environ.get("INCORRECT_PASSWORD_1"),
            False,
            True,
        ),
        (  # captcha is visible after three times incorrect login total quantity - use enter key
            os.environ.get("INCORRECT_EMAIL_4"),
            os.environ.get("INCORRECT_PASSWORD_1"),
            os.environ.get("INCORRECT_EMAIL_1"),
            os.environ.get("INCORRECT_PASSWORD_3"),
            os.environ.get("INCORRECT_EMAIL_1"),
            os.environ.get("INCORRECT_PASSWORD_4"),
            True,
            True,
        ),
    ],
)
def test_TS01_failed_login_captcha_functionality(
    request,
    driver,
    base_url,
    user_first,
    password_first,
    user_second,
    password_second,
    user_third,
    password_third,
    enter_key,
    one_correct_login,
):
    # given
    login_page = LoginPage(driver=driver, base_url=base_url)

    try:
        if const.LOGIN_ENDPOINT in driver.current_url:
            login_page.assert_path_in_current_url(path=const.LOGIN_ENDPOINT)

        elif const.AFTER_LOGIN_ENDPOINT_DOCTOR_PAGE in driver.current_url:
            login_page.assert_path_in_current_url(path=const.LOGIN_ENDPOINT_DOCTOR_PAGE)

        elif const.DOCTOR_PAGE in driver.current_url:
            login_page.click_on(by_loctor=ForDoctorsPage.BANNER_X_CHAR)

        # when
        login_page.incorrect_login_as(
            username=user_first,
            password=password_first,
            enter_key=enter_key
        )
        login_page.assert_path_in_current_url(path=const.VALIDATION_ENDPOINT)
        login_page.incorrect_login_as(
            username=user_second,
            password=password_second,
            enter_key=enter_key
        )

        if one_correct_login:
            login_page.login_as(
                username=os.environ.get("USER_EMAIL"),
                password=os.environ.get("PASSWORD"),
                enter_key=True,
            )
            login_page.click_on(by_loctor=LoginPageLocators.ICON_ACCOUNT)
            login_page.click_on(by_loctor=LoginPageLocators.LOGOUT_BUTTON)
            time.sleep(1)

        login_page.incorrect_login_as(
            username=user_third,
            password=password_third,
            enter_key=enter_key
        )

        # then
        login_page.click_on(by_loctor=LoginPageLocators.CAPTCHA_SECTION)
        print(f"{request.node.name} is done " + "\U0001F44D")

    except Exception:
        login_page.do_screenshot(name=request.node.name)
        raise
