from resources.locators import HomePageLocators, LoginPageLocators
from resources.page_object.login_page import LoginPage
from resources.validation_text_data import ValidationTextData as TXT


def test_TS01_TC001_successful_login_with_username(request, driver, test_data):
    login_page = LoginPage(driver=driver)
    login_page.assert_path_in_current_url(path=TXT.LOGIN_ENDPOINT)
    login_page.login_as(username=test_data["user_name"], password=test_data["password"], submit=True)
    login_page.assert_path_in_current_url(path=TXT.AFTER_LOGIN_ENDPOINT)
    login_page.click_on(HomePageLocators.ICON_ACCOUNT)
    assert login_page.element_is_visible(LoginPageLocators.LOGOUT_BUTTON) is True
    login_page.assert_element_text(LoginPageLocators.LOGOUT_BUTTON, TXT.LOGOUT_BUTTON)
    login_page.click_on_and_wait_for_a_new_page(LoginPageLocators.LOGOUT_BUTTON)
    assert login_page.element_is_visible(LoginPageLocators.SUBMIT_BUTTON) is True
    login_page.assert_element_text(LoginPageLocators.SUBMIT_BUTTON, TXT.LOGIN_BUTTON)
