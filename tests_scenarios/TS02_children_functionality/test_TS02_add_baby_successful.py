import pytest

from resources.automation_methods import AutomationMethods
from resources.locators import AddBabyLocators, ListOfChildrenLocators
from resources.page_object.add_baby_page import AddBabyPage
from resources.validation_text_data import ValidationTextData as txt



@pytest.mark.parametrize("number_of_days", [60])
@pytest.mark.add_baby
def test_TS02_successful_add_baby(request, driver, number_of_days):
    try:
        add_baby_page = AddBabyPage(driver=driver)
        add_baby_page.assert_path_in_current_url(path=txt.ADD_BABY_ENDPOINT)

        add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)

        add_baby_page.assert_element_color_hex(
            by_locator=AddBabyLocators.I_AM_PREGNANT, color_hex=txt.ALERT_COLOR
        )

        add_baby_page.click_on(by_loctor=AddBabyLocators.I_AM_PREGNANT)

        add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)

        add_baby_page.assert_element_color_hex(
            by_locator=AddBabyLocators.NO_GENDER_RADIO, color_hex=txt.ALERT_COLOR
        )

        add_baby_page.click_on(by_loctor=AddBabyLocators.NO_GENDER_RADIO)

        add_baby_page.assert_element_text_in_page_source(
            element_text=txt.REQUIRED_FIELD
        )
        assert add_baby_page.element_is_visible(AddBabyLocators.ALERT_MESSAGE) is True

        assert (
                add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_DAY) is True
        )
        assert (
                add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_MONTH)
                is True
        )
        assert (
                add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_YEAR) is True
        )

        future_date: dict = AutomationMethods().get_date_from_delta_n_day(
            add_days=number_of_days
        )
        future_day = future_date["day"]
        future_month = future_date["month"]
        year = future_date["year"]
        add_baby_page.select_date(
            day=future_day, month=future_month, year=year, pregnant=True
        )

        assert (
                add_baby_page.element_is_visible(
                    by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT
                )
                is True
        )
        add_baby_page.assert_element_text_in_page_source(element_text=txt.I_ACCEPT)

        add_baby_page.click_on_and_wait_for_a_new_page(
            by_loctor=AddBabyLocators.ADD_BABY_BUTTON
        )

        add_baby_page.assert_path_in_current_url(path=txt.CHILDREN_LIST_ENDPOINT)

        assert (
                add_baby_page.element_is_visible(
                    by_locator=ListOfChildrenLocators.ALERT_ICON
                )
                is True
        )
        assert (
                add_baby_page.element_is_visible(
                    by_locator=ListOfChildrenLocators.ALERT_CONTENT
                )
                is True
        )
        add_baby_page.assert_element_text(
            by_locator=ListOfChildrenLocators.ALERT_CONTENT,
            element_text=txt.CORRECT_ADDED_BABY_ALERT,
        )

        assert (
                add_baby_page.element_is_visible(
                    by_locator=ListOfChildrenLocators.IMG_STORK
                )
                is True
        )
        add_baby_page.assert_element_text_in_page_source(element_text=txt.IMG_STORK)

        add_baby_page.assert_element_text(
            by_locator=ListOfChildrenLocators.FIRST_NAME_RENDER,
            element_text=txt.NO_NAME,
        )
        add_baby_page.assert_element_text_in_page_source(element_text=txt.NO_NAME)
        add_baby_page.assert_element_text(
            by_locator=ListOfChildrenLocators.CONFIRM_DATE_OF_BIRTH_LINK,
            element_text=txt.CONFIRM_BABY_BORN_DATE,
        )
        assert (
                add_baby_page.is_clickable(
                    by_locator=ListOfChildrenLocators.CONFIRM_DATE_OF_BIRTH_LINK
                )
                is True
        )
        add_baby_page.assert_element_text_in_page_source(
            element_text=txt.CONFIRM_BABY_BORN_DATE
        )

        date_of_birth = f"{future_day}.{future_month}.{year}"
        assert (
                date_of_birth
                == add_baby_page.get_element(
            by_locator=ListOfChildrenLocators.DATE_OF_BIRTH_REGULAR
        ).text
        )
        add_baby_page.assert_element_text_in_page_source(element_text=date_of_birth)

        add_baby_page.assert_element_text(
            by_locator=ListOfChildrenLocators.GENDER_SECTION, element_text=txt.NO_GENDER
        )
        assert (
                txt.NO_GENDER
                in add_baby_page.get_element(
            by_locator=ListOfChildrenLocators.GENDER_SECTION
        ).text
        )
        add_baby_page.assert_element_text_in_page_source(
            element_text=txt.NO_GENDER[-8:]
        )
        assert (
                txt.NO_BORN_GIFT[-3:]
                in add_baby_page.get_element(
            by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO
        ).text
        )
        add_baby_page.assert_element_text(
            by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO,
            element_text=txt.NO_BORN_GIFT,
        )

    except:
        add_baby_page.do_screenshot(name=request.node.name)
        raise
