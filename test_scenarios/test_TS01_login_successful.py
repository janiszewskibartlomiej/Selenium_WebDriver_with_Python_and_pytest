import os
import time

import pyautogui
import pytest

import resources.constants as const
from resources.automation_functions import removing_directories_in_reports_by_number_of_day
from resources.locators import LoginPageLocators, FacebookPage, ForDoctorsPage
from resources.page_object.login_page import LoginPage

removing_directories_in_reports_by_number_of_day(
    n_day=int(os.environ.get("REMOVING_REPORTS_BY_NUMBER_OF_DAY"))
)

user_name: dict = {
    "home_page": os.environ.get("USER_NAME"),
    "doctor_page": os.environ.get("USER_NAME_DOCTOR_PAGE"),
}


@pytest.mark.login
@pytest.mark.parametrize(
    "user, password, enter_key, login_by_facebook",
    [
        (  # login by user name, submit enter
                user_name,
                os.environ.get("PASSWORD"),
                True,
                False,
        ),
        (  # login by user name, submit click
                user_name,
                os.environ.get("PASSWORD"),
                False,
                False,
        ),
        (  # login by email, submit enter
                os.environ.get("USER_EMAIL"),
                os.environ.get("PASSWORD"),
                True,
                False,
        ),
        (  # login by email, submit click
                os.environ.get("USER_EMAIL"),
                os.environ.get("PASSWORD"),
                False,
                False,
        ),
        (  # login by email - upper case, submit enter
                os.environ.get("USER_EMAIL").upper(),
                os.environ.get("PASSWORD"),
                True,
                False,
        ),
        (  # login by email - upper case, submit click
                os.environ.get("USER_EMAIL").upper(),
                os.environ.get("PASSWORD"),
                False,
                False,
        ),
        (  # login by email - capitalize, submit enter
                os.environ.get("USER_EMAIL").capitalize(),
                os.environ.get("PASSWORD"),
                True,
                False
        ),
        (  # login by email - capitalize, submit click
                os.environ.get("USER_EMAIL").capitalize(),
                os.environ.get("PASSWORD"),
                False,
                False
        ),
        (  # login by facebook
                os.environ.get("USER_EMAIL"),
                os.environ.get("PASSWORD"),
                False,
                True,
        ),
    ],
)
def test_TS01_successful_login(
        request,
        driver,
        base_url,
        user,
        password,
        enter_key,
        login_by_facebook
):
    # given
    login_page = LoginPage(base_url=base_url, driver=driver)
    if const.DOCTOR_PAGE in driver.current_url:
        login_page.click_on(by_loctor=ForDoctorsPage.BANNER_X_CHAR)

    try:
        login_page.assert_path_in_current_url(path=login_page.endpoint)
        username_input = login_page.get_element(
            by_locator=LoginPageLocators.USERNAME_FIELD
        )
        assert username_input.tag_name == const.INPUT_TAG
        password_input = login_page.get_element(
            by_locator=LoginPageLocators.PASSWORD_FIELD
        )
        assert password_input.tag_name == const.INPUT_TAG

        # when
        if login_by_facebook and const.DOCTOR_PAGE not in driver.current_url:

            login_page.open_new_tab_and_switch()
            login_page.driver.get(const.FACEBOOK_PAGE)

            # accept FB role
            pyautogui.hotkey("enter")
            time.sleep(2)

            if login_page.driver.title == const.ERROR:
                login_page.click_on_and_wait_for_a_new_page(by_loctor=FacebookPage.GO_BACK)

            if const.REFRESH_PAGE in login_page.driver.page_source:
                login_page.click_on(by_loctor=FacebookPage.REFRESHE_BUTTON)

            login_page.enter_text(
                by_locator=FacebookPage.EMAIL,
                text=os.environ.get("FACEBOOK_EMAIL")
            )

            login_page.enter_text_and_click_enter(
                by_locators=FacebookPage.PASSWORD,
                text=os.environ.get("FACEBOOK_PASSWORD")
            )

            pyautogui.hotkey("enter")
            time.sleep(3)

            while not login_page.page_is_loading():
                continue

            get_tabs = driver.window_handles
            login_page.driver.switch_to.window(get_tabs[0])

            login_page.click_on_and_wait_for_a_new_page(
                by_loctor=LoginPageLocators.LOGIN_BY_FACEBOOK
            )

            pyautogui.hotkey("enter")

        else:
            if isinstance(user, dict) is True:
                if const.DOCTOR_PAGE in driver.current_url:
                    user = user["doctor_page"]
                else:
                    user = user["home_page"]
            login_page.login_as(
                username=user,
                password=password,
                enter_key=enter_key
            )

        if const.AFTER_LOGIN_ENDPOINT in driver.current_url:
            login_page.assert_path_in_current_url(path=const.AFTER_LOGIN_ENDPOINT)
        elif const.AFTER_LOGIN_ENDPOINT_DOCTOR_PAGE in driver.current_url:
            login_page.assert_path_in_current_url(
                path=const.AFTER_LOGIN_ENDPOINT_DOCTOR_PAGE
            )

        login_page.click_on(LoginPageLocators.ICON_ACCOUNT)
        drop_down = login_page.get_element(
            by_locator=LoginPageLocators.DROP_DOWN_SECTION
        )

        # then
        assert const.LOGIN_INFORMATION_IN_DROPDOWN in drop_down.get_attribute("innerHTML")
        login_page.assert_element_text_in_page_source(
            element_text=const.LOGIN_INFORMATION_IN_DROPDOWN
        )
        assert login_page.element_is_visible(LoginPageLocators.LOGOUT_BUTTON) is True
        login_page.assert_element_text(
            LoginPageLocators.LOGOUT_BUTTON, const.LOGOUT_BUTTON
        )
        login_page.assert_element_text_in_page_source(element_text=const.LOGOUT_BUTTON)
        login_page.click_on_and_wait_for_a_new_page(LoginPageLocators.LOGOUT_BUTTON)
        assert login_page.element_is_visible(LoginPageLocators.SUBMIT_BUTTON) is True
        login_page.assert_element_text(
            LoginPageLocators.SUBMIT_BUTTON, const.LOGIN_BUTTON
        )
        print("User >> ", user)
        print(f"{request.node.name} is done " + "\U0001F44D")

    except Exception:
        login_page.do_screenshot(name=request.node.name)
        raise
