import os

import pytest

import resources.constants as const
from resources.automation_functions import removing_directories_in_reports_by_number_of_day
from resources.locators import LoginPageLocators, ForDoctorsPage
from resources.page_object.login_page import LoginPage

removing_directories_in_reports_by_number_of_day(
    n_day=int(os.environ.get("REMOVING_REPORTS_BY_NUMBER_OF_DAY"))
)


@pytest.mark.login
@pytest.mark.parametrize(
    "user, password, enter_key",
    [
        (  # correct email and incorrect password
                os.environ.get("USER_EMAIL"),
                os.environ.get("INCORRECT_PASSWORD_1"),
                False,
        ),
        (  # correct email and incorrect password
                os.environ.get("USER_EMAIL"),
                os.environ.get("INCORRECT_PASSWORD_2"),
                True,
        ),
        (  # incorrect email and correct password
                os.environ.get("INCORRECT_EMAIL_1"),
                os.environ.get("PASSWORD"),
                False,
        ),
        (  # incorrect email and correct password
                os.environ.get("INCORRECT_EMAIL_2"),
                os.environ.get("PASSWORD"),
                True,
        ),
        (  # correct email and correct password with space key
                " " + os.environ.get("USER_EMAIL"),
                " " + os.environ.get("PASSWORD"),
                False
        ),
        (  # correct email and correct password with space key
                " " + os.environ.get("USER_EMAIL"),
                " " + os.environ.get("PASSWORD"),
                True
        ),
        (  # email and password are left blank
                "",
                "",
                False
        ),
        (  # email and password are left blank
                "",
                "",
                True
        ),
        (  # email and password are white space
                " ",
                " ",
                False
        ),
        (  # email and password are white space
                " ",
                " ",
                True
        ),
        (  # reverse data input
                os.environ.get("PASSWORD"),
                os.environ.get("USER_EMAIL"),
                False
        ),
        (  # reverse data input
                os.environ.get("PASSWORD"),
                os.environ.get("USER_EMAIL"),
                True
        ),
    ],
)
def test_TS01_failed_login(
        request,
        driver,
        base_url,
        user,
        password,
        enter_key
):
    # given
    login_page = LoginPage(driver=driver, base_url=base_url)
    # when
    if const.DOCTOR_PAGE in driver.current_url:
        login_page.click_on(by_loctor=ForDoctorsPage.BANNER_X_CHAR)

    try:
        # Than
        login_page.assert_path_in_current_url(path=login_page.endpoint)
        login_page.assert_element_text(
            LoginPageLocators.SUBMIT_BUTTON,
            const.LOGIN_BUTTON
        )

        # when
        login_page.incorrect_login_as(
            username=user,
            password=password,
            enter_key=enter_key
        )

        # then
        login_page.assert_path_in_current_url(path=login_page.endpoint)
        login_page.click_on(LoginPageLocators.ICON_ACCOUNT)
        assert (
                login_page.element_is_visible(
                    LoginPageLocators.LOGIN_BUTTON_IN_DROP_DOWN_SECTION
                )
                is True
        )
        login_page.assert_element_text(
            LoginPageLocators.LOGIN_BUTTON_IN_DROP_DOWN_SECTION, const.LOGIN_BUTTON
        )
        print(f"{request.node.name} is done " + "\U0001F44D")

    except Exception:
        login_page.do_screenshot(name=request.node.name)
        raise
