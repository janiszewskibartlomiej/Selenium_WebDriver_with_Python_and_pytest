from resources.automation_methods import AutomationMethods

if __name__ == '__main__':
    automation_of_tests = AutomationMethods()
    automation_of_tests.removing_directories_in_reports_by_number_of_day(n_day=7)
    reports = automation_of_tests.run_pytest_html_and_allure_report(by_name="")
    config_path = automation_of_tests.get_path_from_file_name(file_name="config.cfg")
    automation_of_tests.send_email(files=reports)
