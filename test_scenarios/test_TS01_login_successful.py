import pytest

from resources.automation_methods import AutomationMethods
from resources.locators import LoginPageLocators
from resources.page_object.login_page import LoginPage
from resources.validation_text_data import ValidationTextData as txt

test_data: dict = AutomationMethods().get_section_from_config(
    section_list=["Common_data", "Staging"]
)


def user() -> str:
    login_page = LoginPage(driver=AutomationMethods().get_driver())
    return login_page.get_user_name()


def facebook() -> bool:
    user_name = user()
    if user_name == test_data["user_name_doctor_page"]:
        return False
    else:
        return True


user_name = user()
facebook_login = facebook()


@pytest.mark.login
@pytest.mark.parametrize(
    "user, password, enter_key, login_by_facebook",
    [
        (
                user_name,
                test_data["password"],
                True,
                False,
        ),  # login by user name, submit enter
        (
                user_name,
                test_data["password"],
                False,
                False,
        ),  # login by user name, submit click
        (
                test_data["user_email"],
                test_data["password"],
                True,
                False,
        ),  # login by email, submit enter
        (
                test_data["user_email"],
                test_data["password"],
                False,
                False,
        ),  # login by email, submit click
        (
                test_data["user_email"].upper(),
                test_data["password"],
                True,
                False,
        ),  # login by email - upper case, submit enter
        (
                test_data["user_email"].upper(),
                test_data["password"],
                False,
                False,
        ),  # login by email - upper case, submit click
        (test_data["user_email"].capitalize(), test_data["password"], True, False),
        # login by email - capitalize, submit enter
        (test_data["user_email"].capitalize(), test_data["password"], False, False),
        # login by email - capitalize, submit click
        (
                test_data["user_email"],
                test_data["password"],
                False,
                facebook_login,
        ),  # login by facebook
    ],
)
def test_TS01_successful_login(
        request, driver, user, password, enter_key, login_by_facebook
):
    try:
        # given
        login_page = LoginPage(driver=driver)
        login_page.assert_path_in_current_url(path=login_page.endpoint)
        username_input = login_page.get_element(
            by_locator=LoginPageLocators.USERNAME_FIELD
        )
        assert username_input.tag_name == txt.INPUT_TAG
        password_input = login_page.get_element(
            by_locator=LoginPageLocators.PASSWORD_FIELD
        )
        assert password_input.tag_name == txt.INPUT_TAG

        # when
        if login_by_facebook:
            login_page.click_on_and_wait_for_a_new_page(
                by_loctor=LoginPageLocators.LOGIN_BY_FACEBOOK
            )
            login_page.enter_text(
                by_locator=LoginPageLocators.FACEBOOK_EMAIL,
                text=test_data["facebook_email"],
            )
            login_page.enter_text(
                by_locator=LoginPageLocators.FACEBOOK_PASSWORD,
                text=test_data["facebook_password"],
            )
            login_page.click_on_and_wait_for_a_new_page(
                by_loctor=LoginPageLocators.FACEBOOK_LOGIN_BUTTON
            )
        else:
            login_page.login_as(username=user, password=password, enter_key=enter_key)

        if txt.AFTER_LOGIN_ENDPOINT in driver.current_url:
            login_page.assert_path_in_current_url(path=txt.AFTER_LOGIN_ENDPOINT)
        elif txt.AFTER_LOGIN_ENDPOINT_DOCTOR_PAGE in driver.current_url:
            login_page.assert_path_in_current_url(path=txt.AFTER_LOGIN_ENDPOINT_DOCTOR_PAGE)

        login_page.click_on(LoginPageLocators.ICON_ACCOUNT)
        drop_down = login_page.get_element(
            by_locator=LoginPageLocators.DROP_DOWN_SECTION
        )

        # then
        assert txt.LOGIN_INFORMATION_IN_DROPDOWN in drop_down.get_attribute("innerHTML")
        login_page.assert_element_text_in_page_source(
            element_text=txt.LOGIN_INFORMATION_IN_DROPDOWN
        )
        assert login_page.element_is_visible(LoginPageLocators.LOGOUT_BUTTON) is True
        login_page.assert_element_text(
            LoginPageLocators.LOGOUT_BUTTON, txt.LOGOUT_BUTTON
        )
        login_page.assert_element_text_in_page_source(element_text=txt.LOGOUT_BUTTON)
        login_page.click_on_and_wait_for_a_new_page(LoginPageLocators.LOGOUT_BUTTON)
        assert login_page.element_is_visible(LoginPageLocators.SUBMIT_BUTTON) is True
        login_page.assert_element_text(
            LoginPageLocators.SUBMIT_BUTTON, txt.LOGIN_BUTTON
        )
        print(f"{request.node.name} is done " + "\U0001F44D")
    except:
        login_page.do_screenshot(name=request.node.name)
        raise
