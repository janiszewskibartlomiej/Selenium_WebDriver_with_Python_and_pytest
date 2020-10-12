import pytest

from resources.automation_methods import AutomationMethods
from resources.locators import LoginPageLocators
from resources.page_object.login_page import LoginPage
from resources.validation_text_data import ValidationTextData as txt

AutomationMethods().removing_directories_in_reports_by_number_of_day(n_day=7)

data = AutomationMethods().get_section_from_config(
    section_list=["Common_data", "Staging"]
)


@pytest.mark.captcha
@pytest.mark.parametrize(
    "user_first, password_first, "
    "user_second, password_second, "
    "user_third, password_third, "
    "enter_key, one_correct_login",
    [
        (
            data["incorrect_email_1"],
            data["incorrect_password_1"],
            data["incorrect_email_2"],
            data["incorrect_password_2"],
            data["incorrect_email_3"],
            data["incorrect_password_3"],
            False,
            False,
        ),  # captcha is visible after three times incorrect login
        (
            data["incorrect_email_1"],
            data["incorrect_password_1"],
            data["incorrect_email_2"],
            data["incorrect_password_2"],
            data["incorrect_email_3"],
            data["incorrect_password_3"],
            True,
            False,
        ),  # captcha is visible after three times incorrect login - use enter key
        (
            data["incorrect_email_4"],
            data["incorrect_password_4"],
            data["incorrect_email_1"],
            data["incorrect_password_2"],
            data["incorrect_email_3"],
            data["incorrect_password_1"],
            False,
            True,
        ),  # captcha is visible after three times incorrect login total quantity
        (
            data["incorrect_email_4"],
            data["incorrect_password_1"],
            data["incorrect_email_1"],
            data["incorrect_password_3"],
            data["incorrect_email_2"],
            data["incorrect_password_4"],
            True,
            True,
        ),  # captcha is visible after three times incorrect login total quantity - use enter key
    ],
)
def test_TS01_failed_login_captcha_functionality(
    request,
    driver,
    base_url,
    test_data_from_fixture,
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
        if txt.LOGIN_ENDPOINT in driver.current_url:
            login_page.assert_path_in_current_url(path=txt.LOGIN_ENDPOINT)
        elif txt.AFTER_LOGIN_ENDPOINT_DOCTOR_PAGE in driver.current_url:
            login_page.assert_path_in_current_url(path=txt.LOGIN_ENDPOINT_DOCTOR_PAGE)

        # when
        login_page.incorrect_login_as(
            username=user_first, password=password_first, enter_key=enter_key
        )
        login_page.assert_path_in_current_url(path=txt.VALIDATION_ENDPOINT)
        login_page.incorrect_login_as(
            username=user_second, password=password_second, enter_key=enter_key
        )

        if one_correct_login:
            login_page.login_as(
                username=test_data_from_fixture["user_email"],
                password=test_data_from_fixture["password"],
                enter_key=True,
            )
            login_page.click_on(by_loctor=LoginPageLocators.ICON_ACCOUNT)
            login_page.click_on(by_loctor=LoginPageLocators.LOGOUT_BUTTON)

        login_page.incorrect_login_as(
            username=user_third, password=password_third, enter_key=enter_key
        )

        # then
        login_page.click_on(by_loctor=LoginPageLocators.CAPTCHA_SECTION)
        print(f"{request.node.name} is done " + "\U0001F44D")

    except Exception:
        login_page.do_screenshot(name=request.node.name)
        raise
