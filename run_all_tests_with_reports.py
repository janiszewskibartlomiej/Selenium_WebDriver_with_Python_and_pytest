import os
import sys

sys.path.append("..")
import tests.resources.constants as const

from tests.resources.automation_functions import (
    removing_directories_in_reports_by_number_of_day,
    run_pytest_html_and_allure_report,
    send_email
)

if __name__ == "__main__":
    removing_directories_in_reports_by_number_of_day(
        n_day=int(os.environ.get("REMOVING_REPORTS_BY_NUMBER_OF_DAY"))
    )
    reports = run_pytest_html_and_allure_report()
    send_email(
        send_to=os.environ.get("ADMIN_EMAIL"),
        subject=const.REPORTS_OF_TESTS,
        files=reports
    )






