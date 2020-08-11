import pytest

from resources.automation_methods import AutomationMethods
from resources.locators import LoginPageLocators, HomePageLocators
from resources.page_object.home_page import HomePage
from resources.page_object.login_page import LoginPage
from resources.validation_text_data import ValidationTextData as txt

test_data: dict = AutomationMethods().get_section_from_config(
    section_list=["Common_data", "Staging"]
)


@pytest.mark.parametrize(
    "user_first, password_first, "
    "user_second, password_second, "
    "user_third, password_third, "
    "enter_key, one_correct_login",
    [
        (
            test_data["incorrect_email_1"],
            test_data["incorrect_password_1"],
            test_data["incorrect_email_2"],
            test_data["incorrect_password_2"],
            test_data["incorrect_email_3"],
            test_data["incorrect_password_3"],
            False,
            False,
        ),  # captcha is visible after three times incorrect login
        (
            test_data["incorrect_email_1"],
            test_data["incorrect_password_1"],
            test_data["incorrect_email_2"],
            test_data["incorrect_password_2"],
            test_data["incorrect_email_3"],
            test_data["incorrect_password_3"],
            True,
            False,
        ),  # captcha is visible after three times incorrect login - use enter key
        (
            test_data["incorrect_email_4"],
            test_data["incorrect_password_4"],
            test_data["incorrect_email_1"],
            test_data["incorrect_password_2"],
            test_data["incorrect_email_3"],
            test_data["incorrect_password_1"],
            False,
            True,
        ),  # captcha is visible after three times incorrect login total quantity
        (
            test_data["incorrect_email_4"],
            test_data["incorrect_password_1"],
            test_data["incorrect_email_1"],
            test_data["incorrect_password_3"],
            test_data["incorrect_email_2"],
            test_data["incorrect_password_4"],
            True,
            True,
        ),  # captcha is visible after three times incorrect login total quantity - use enter key
    ],
)
@pytest.mark.captcha
def test_TS01_failed_login_captcha_functionality(
    request,
    driver,
    test_data,
    user_first,
    password_first,
    user_second,
    password_second,
    user_third,
    password_third,
    enter_key,
    one_correct_login,
):
    try:
        home_page = HomePage(driver=driver)
        home_page.click_on(by_loctor=HomePageLocators.ICON_ACCOUNT)
        home_page.click_on_and_wait_for_a_new_page(
            by_loctor=HomePageLocators.LOGIN_BUTTON_IN_DROP_DOWN_SECTION
        )
        home_page.assert_path_in_current_url(path=txt.LOGIN_ENDPOINT)
        login_page = LoginPage(driver=driver)
        login_page.incorrect_login_as(
            username=user_first, password=password_first, enter_key=enter_key
        )
        login_page.assert_path_in_current_url(path=txt.VALIDATION_ENDPOINT)
        login_page.incorrect_login_as(
            username=user_second, password=password_second, enter_key=enter_key
        )

        if one_correct_login:
            login_page.login_as(
                username=test_data["user_email"],
                password=test_data["password"],
                enter_key=True,
            )
            login_page.click_on(by_loctor=LoginPageLocators.ICON_ACCOUNT)
            login_page.click_on(by_loctor=LoginPageLocators.LOGOUT_BUTTON)

        login_page.incorrect_login_as(
            username=user_third, password=password_third, enter_key=enter_key
        )
        login_page.click_on(by_loctor=LoginPageLocators.CAPTCHA_SECTION)
    except:
        login_page.do_screenshot(name=request.node.name)
        raise
