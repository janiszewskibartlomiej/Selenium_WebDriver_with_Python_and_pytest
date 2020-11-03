<h3>AUTOMATION TESTS</h3>

Language : Python 3.8 up >> https://www.python.org/downloads/

#### External libraries == `requirements-test.txt`
* selenium
* pytest
* pytest-html
* allure-pytest
* pytest-xdist
* webdriver-manager


#### install allure-pytest in console >> https://docs.qameta.io/allure/#_installing_a_commandline

#### run allure report from zip file >> Before unzip we must start server like `python -m http.server`


#### install command == `pip install -r requirements.txt`
#### run tests in command line == `pytest -v`run test with report = python run_all_tests_with_reports.py

#### If we have failed any tests I think we can run tests one more time with flag - last failed test  run command == `pytest --lf`
Please creating .env file with data >> example in `.env.example`