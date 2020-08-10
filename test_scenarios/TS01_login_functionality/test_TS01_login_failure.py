import pytest

from resources.automation_methods import AutomationMethods
from resources.locators import LoginPageLocators
from resources.page_object.login_page import LoginPage
from resources.validation_text_data import ValidationTextData as txt

test_data: dict = AutomationMethods().get_section_from_config(section_list=["Common_data", "Staging"])


@pytest.mark.parametrize("user, password, enter_key, login_by_facebook", [
    (test_data["user_email"], test_data["incorrect_password_1"], False, False),  # correct email and incorrect password
    (test_data["user_email"], test_data["incorrect_password_2"], True, False),  # correct email and incorrect password
    (test_data["incorrect_email_1"], test_data["password"], False, False),  # incorrect email and correct password
    (test_data["incorrect_email_2"], test_data["password"], True, False),  # incorrect email and correct password
    (' ' + test_data["user_email"], ' ' + test_data["password"], False, False),
    # correct email and correct password with space key
    (' ' + test_data["user_email"], ' ' + test_data["password"], True, False),
    # correct email and correct password with space key
    ('', '', False, False),  # email and password are left blank
    ('', '', True, False),  # email and password are left blank
    (' ', ' ', False, False),  # email and password are white space
    (' ', ' ', True, False),  # email and password are white space
    (test_data["password"], test_data["user_email"], False, False),  # reverse data input
    (test_data["password"], test_data["user_email"], True, False)  # reverse data input
])
@pytest.mark.login
def test_TS01_failed_login(request, driver, user, password, enter_key, login_by_facebook):
    try:
        login_page = LoginPage(driver=driver)
        login_page.assert_path_in_current_url(path=txt.LOGIN_ENDPOINT)
        login_page.visit_page(endpoit=txt.LOGIN_ENDPOINT)
        login_page.assert_path_in_current_url(path=txt.LOGIN_ENDPOINT)
        login_page.assert_element_text(LoginPageLocators.SUBMIT_BUTTON, txt.LOGIN_BUTTON)
        login_page.incorrect_login_as(username=user, password=password, enter_key=enter_key)
        login_page.assert_path_in_current_url(path=txt.LOGIN_ENDPOINT)
        login_page.click_on(LoginPageLocators.ICON_ACCOUNT)
        assert login_page.element_is_visible(LoginPageLocators.LOGIN_BUTTON_IN_DROP_DOWN_SECTION) is True
        login_page.assert_element_text(LoginPageLocators.LOGIN_BUTTON_IN_DROP_DOWN_SECTION, txt.LOGIN_BUTTON)
    except:
        login_page.do_screenshot(name=request.node.name)
        raise
