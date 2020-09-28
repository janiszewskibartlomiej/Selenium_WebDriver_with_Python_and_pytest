import pytest

from resources.automation_methods import AutomationMethods
from resources.locators import AddBabyLocators, ListOfChildrenLocators
from resources.page_object.add_baby_page import AddBabyPage
from resources.page_object.typo3_page import Typo3Page
from resources.validation_text_data import ValidationTextData as txt

add_baby_locators = AddBabyLocators()


@pytest.mark.parametrize("pregnant_or_baby_born_radio, "
                         "gender_radio, "
                         "baby_name, "
                         "gift, "
                         "number_of_days",
                         [
                             (
                                     add_baby_locators.I_AM_PREGNANT,
                                     add_baby_locators.NO_GENDER_RADIO,
                                     txt.NO_NAME,
                                     False,
                                     60
                             )
                         ]
                         )
@pytest.mark.add_baby
def test_TS02_successful_add_baby(request, driver, pregnant_or_baby_born_radio, gender_radio, baby_name, gift,
                                  number_of_days):
    add_baby_page = AddBabyPage(driver=driver)
    if "dlalekarzy" not in add_baby_page.driver.current_url:
        try:
            # given
            add_baby_page.assert_path_in_current_url(path=txt.ADD_BABY_ENDPOINT)

            # when
            add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)

            add_baby_page.assert_element_color_hex(
                by_locator=AddBabyLocators.I_AM_PREGNANT, color_hex=txt.ALERT_COLOR
            )

            # pregnant_or_baby_born_radio
            add_baby_page.click_on(by_loctor=pregnant_or_baby_born_radio)

            add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)

            add_baby_page.assert_element_color_hex(
                by_locator=AddBabyLocators.NO_GENDER_RADIO, color_hex=txt.ALERT_COLOR
            )

            # gender_radio
            add_baby_page.click_on(by_loctor=gender_radio)

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

            if pregnant_or_baby_born_radio == add_baby_locators.I_AM_PREGNANT:
                pregnant = True
            else:
                pregnant = False

            add_baby_page.select_date(
                day=future_day, month=future_month, year=year, pregnant=pregnant
            )

            if pregnant is True or number_of_days < 46:
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

            # then
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
            # pregnant
            if pregnant_or_baby_born_radio == add_baby_locators.I_AM_PREGNANT:
                assert (
                        add_baby_page.element_is_visible(
                            by_locator=ListOfChildrenLocators.IMG_STORK
                        )
                        is True
                )
                add_baby_page.assert_element_text_in_page_source(element_text=txt.IMG_STORK)

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

            # baby name
            add_baby_page.assert_element_text(
                by_locator=ListOfChildrenLocators.FIRST_NAME_RENDER,
                element_text=baby_name,
            )
            add_baby_page.assert_element_text_in_page_source(element_text=baby_name)

            # date of born
            date_of_birth = f"{future_day}.{future_month}.{year}"
            assert (
                    date_of_birth
                    == add_baby_page.get_element(
                by_locator=ListOfChildrenLocators.DATE_OF_BIRTH_REGULAR
            ).text
            )
            add_baby_page.assert_element_text_in_page_source(element_text=date_of_birth)

            # gender
            all_gender_text, gender_text = None, None
            if gender_radio == add_baby_locators.NO_GENDER_RADIO:
                all_gender_text = txt.NO_GENDER
                gender_text = all_gender_text[-8:]
            elif gender_radio == add_baby_locators.MALE:
                all_gender_text = txt.MALE_GENDER
                gender_text = all_gender_text[-8:]
            elif gender_radio == add_baby_locators.FEMALE:
                all_gender_text = txt.FEMALE_GENDER
                gender_text = all_gender_text[-11:]

            add_baby_page.assert_element_text(
                by_locator=ListOfChildrenLocators.GENDER_SECTION, element_text=all_gender_text
            )
            assert (
                    all_gender_text
                    in add_baby_page.get_element(
                by_locator=ListOfChildrenLocators.GENDER_SECTION
            ).text
            )
            add_baby_page.assert_element_text_in_page_source(
                element_text=gender_text
            )

            # gift
            if gift:
                all_born_gift_text = txt.BORN_GIFT_YES
            else:
                all_born_gift_text = txt.NO_BORN_GIFT
            gift_text = all_born_gift_text[-3:]

            assert (
                    gift_text
                    in add_baby_page.get_element(
                by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO
            ).text
            )
            add_baby_page.assert_element_text(
                by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO,
                element_text=all_born_gift_text
            )

            typo3 = Typo3Page(driver=driver)

        except:
            add_baby_page.do_screenshot(name=request.node.name)
            raise
