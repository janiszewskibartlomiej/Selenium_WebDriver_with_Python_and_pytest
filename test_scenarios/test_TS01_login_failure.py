import pytest

from resources.automation_methods import AutomationMethods
from resources.locators import LoginPageLocators
from resources.page_object.login_page import LoginPage
from resources.validation_text_data import ValidationTextData as txt

AutomationMethods().removing_directories_in_reports_by_number_of_day(n_day=7)

test_data: dict = AutomationMethods().get_section_from_config(
    section_list=["Common_data", "Staging"]
)


@pytest.mark.login
@pytest.mark.parametrize(
    "user, password, enter_key",
    [
        (
            test_data["user_email"],
            test_data["incorrect_password_1"],
            False,
        ),  # correct email and incorrect password
        (
            test_data["user_email"],
            test_data["incorrect_password_2"],
            True,
        ),  # correct email and incorrect password
        (
            test_data["incorrect_email_1"],
            test_data["password"],
            False,
        ),  # incorrect email and correct password
        (
            test_data["incorrect_email_2"],
            test_data["password"],
            True,
        ),  # incorrect email and correct password
        (" " + test_data["user_email"], " " + test_data["password"], False),
        # correct email and correct password with space key
        (" " + test_data["user_email"], " " + test_data["password"], True),
        # correct email and correct password with space key
        ("", "", False),  # email and password are left blank
        ("", "", True),  # email and password are left blank
        (" ", " ", False),  # email and password are white space
        (" ", " ", True),  # email and password are white space
        (test_data["password"], test_data["user_email"], False),  # reverse data input
        (test_data["password"], test_data["user_email"], True),  # reverse data input
    ],
)
def test_TS01_failed_login(request, driver, base_url, user, password, enter_key):
    # given
    login_page = LoginPage(driver=driver, base_url=base_url)

    try:
        login_page.assert_path_in_current_url(path=login_page.endpoint)
        login_page.visit_page(endpoit=login_page.endpoint)
        login_page.assert_path_in_current_url(path=login_page.endpoint)
        login_page.assert_element_text(
            LoginPageLocators.SUBMIT_BUTTON, txt.LOGIN_BUTTON
        )

        # when
        login_page.incorrect_login_as(
            username=user, password=password, enter_key=enter_key
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
            LoginPageLocators.LOGIN_BUTTON_IN_DROP_DOWN_SECTION, txt.LOGIN_BUTTON
        )
        print(f"{request.node.name} is done " + "\U0001F44D")

    except Exception:
        login_page.do_screenshot(name=request.node.name)
        raise
