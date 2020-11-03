import os

import pytest

import resources.constants as const
from resources.automation_functions import (
    removing_directories_in_reports_by_number_of_day,
    get_date_from_delta_n_day,
)
from resources.locators import AddBabyLocators, ListOfChildrenLocators
from resources.page_object.add_baby_page import AddBabyPage
from resources.page_object.typo3_page import Typo3Page

removing_directories_in_reports_by_number_of_day(
    n_day=int(os.environ.get("REMOVING_REPORTS_BY_NUMBER_OF_DAY"))
)


@pytest.mark.parametrize(
    "pregnant_or_baby_born_radio, "
    "gender_radio, "
    "baby_name, "
    "gift, "
    "number_of_days",
    [
        (
            AddBabyLocators.I_AM_PREGNANT,
            AddBabyLocators.NO_GENDER_RADIO,
            const.NO_NAME,
            False,
            60,
        )
    ],
)
@pytest.mark.add_baby
def test_TS02_successful_add_baby(
    request,
    base_url,
    driver,
    pregnant_or_baby_born_radio,
    gender_radio,
    baby_name,
    gift,
    number_of_days,
):
    # given
    add_baby_page = AddBabyPage(driver=driver)

    if "dlalekarzy" not in add_baby_page.driver.current_url:

        try:
            add_baby_page.assert_path_in_current_url(path=const.ADD_BABY_ENDPOINT)

            # when
            add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)

            add_baby_page.assert_element_color_hex(
                by_locator=AddBabyLocators.I_AM_PREGNANT, color_hex=const.ALERT_COLOR
            )

            # pregnant_or_baby_born_radio
            add_baby_page.click_on(by_loctor=pregnant_or_baby_born_radio)

            add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)

            add_baby_page.assert_element_color_hex(
                by_locator=AddBabyLocators.NO_GENDER_RADIO, color_hex=const.ALERT_COLOR
            )

            # gender_radio
            add_baby_page.click_on(by_loctor=gender_radio)

            add_baby_page.assert_element_text_in_page_source(
                element_text=const.REQUIRED_FIELD
            )
            assert (
                add_baby_page.element_is_visible(AddBabyLocators.ALERT_MESSAGE) is True
            )

            assert (
                add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_DAY)
                is True
            )
            assert (
                add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_MONTH)
                is True
            )
            assert (
                add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_YEAR)
                is True
            )

            future_date: dict = get_date_from_delta_n_day(add_days=number_of_days)
            future_day = future_date["day"]
            future_month = future_date["month"]
            year = future_date["year"]

            if pregnant_or_baby_born_radio == AddBabyLocators.I_AM_PREGNANT:
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
                add_baby_page.assert_element_text_in_page_source(
                    element_text=const.I_ACCEPT
                )

            add_baby_page.click_on_and_wait_for_a_new_page(
                by_loctor=AddBabyLocators.ADD_BABY_BUTTON
            )

            # then
            add_baby_page.assert_path_in_current_url(path=const.CHILDREN_LIST_ENDPOINT)

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
                element_text=const.CORRECT_ADDED_BABY_ALERT,
            )
            # pregnant
            if pregnant_or_baby_born_radio == AddBabyLocators.I_AM_PREGNANT:
                assert (
                    add_baby_page.element_is_visible(
                        by_locator=ListOfChildrenLocators.IMG_STORK
                    )
                    is True
                )
                add_baby_page.assert_element_text_in_page_source(
                    element_text=const.IMG_STORK
                )

                add_baby_page.assert_element_text(
                    by_locator=ListOfChildrenLocators.CONFIRM_DATE_OF_BIRTH_LINK,
                    element_text=const.CONFIRM_BABY_BORN_DATE,
                )
                assert (
                    add_baby_page.is_clickable(
                        by_locator=ListOfChildrenLocators.CONFIRM_DATE_OF_BIRTH_LINK
                    )
                    is True
                )
                add_baby_page.assert_element_text_in_page_source(
                    element_text=const.CONFIRM_BABY_BORN_DATE
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
            if gender_radio == AddBabyLocators.NO_GENDER_RADIO:
                all_gender_text = const.NO_GENDER
                gender_text = all_gender_text[-8:]
            elif gender_radio == AddBabyLocators.MALE:
                all_gender_text = const.MALE_GENDER
                gender_text = all_gender_text[-8:]
            elif gender_radio == AddBabyLocators.FEMALE:
                all_gender_text = const.FEMALE_GENDER
                gender_text = all_gender_text[-11:]

            add_baby_page.assert_element_text(
                by_locator=ListOfChildrenLocators.GENDER_SECTION,
                element_text=all_gender_text,
            )
            assert (
                all_gender_text
                in add_baby_page.get_element(
                    by_locator=ListOfChildrenLocators.GENDER_SECTION
                ).text
            )
            add_baby_page.assert_element_text_in_page_source(element_text=gender_text)

            # gift
            if gift:
                all_born_gift_text = const.BORN_GIFT_YES
            else:
                all_born_gift_text = const.NO_BORN_GIFT
            gift_text = all_born_gift_text[-3:]

            assert (
                gift_text
                in add_baby_page.get_element(
                    by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO
                ).text
            )
            add_baby_page.assert_element_text(
                by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO,
                element_text=all_born_gift_text,
            )

            typo3 = Typo3Page(driver=driver, base_url=base_url)

        except Exception:
            add_baby_page.do_screenshot(name=request.node.name)
            raise
