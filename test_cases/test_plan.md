What you need:

    Python 3
    Selenium
    pytest
    pytest-html
    allure-pytest
    
    geckodriver.exe >> https://github.com/mozilla/geckodriver/releases/tag/v0.27.0
    chromedriver.exe >> https://chromedriver.chromium.org/downloads
    IEDriverServer.exe only 32 bit ver >> https://www.selenium.dev/downloads/
    selenium-server-standalone-x.xxx.xx.jar >> https://www.selenium.dev/downloads/
    
Run steps:

1. install Python https://www.python.org/downloads/

2. Open terminal and type command: 
    
        1. 'pip install -r requirements.txt'
        3. 'python -v runAllTests.py'
        
3. Download every drivers and add to ./drivers/

geckodriver.exe >> https://github.com/mozilla/geckodriver/releases/tag/v0.27.0

chromedriver.exe >> https://chromedriver.chromium.org/downloads

IEDriverServer.exe only 32 bit ver - is beater >> https://www.selenium.dev/downloads/

selenium-server-standalone-x.xxx.xx.jar >> https://www.selenium.dev/downloads/

    
### System and Browsers

- [x] WIN10 + Chrome 
- [x] WIN10 + FireFox
- [x] WIN10 + Internet Explorer
- [x] Android + Chrome
- [ ] iOS + Safari
- [ ] iPad + Safari
- [ ] macOS + Safari
    
***
| Test Scenario id | Test Scenario name | Test Scenario and Test Case id | Test Case name | Description |
| --- | --- | --- | --- | --- |
| [TS01](#TS01) | Check login functionality | | | |
| | | [TS01_TC001](#TS01_TC001) | Successful login | Using correct username and password |
| | | [TS01_TC002](#TS01_TC002) | Successful login | Using correct email and password |
| | | [TS01_TC003](#TS01_TC003) | Successful login | Using correct email and password - capitalizer |
| | | [TS01_TC009](#TS01_TC009) | Successful login | Using correct facebook acount |
| | | [TS01_TC004](#TS01_TC004) | Failed login | Using correct email and incorrect password |
| | | [TS01_TC005](#TS01_TC005) | Failed login | Using incorrect email and correct password |
| | | [TS01_TC006](#TS01_TC006) | Failed login | Using correct email and password with space key |
| | | [TS01_TC007](#TS01_TC007) | Failed login | Using  email and password are left blank |
| | | [TS01_TC008](#TS01_TC008) | Failed login | Using reverse data input |
| [TS02](#TS02) | Check captcha functionality | | | |
| | | [TS02_TC001](#TS02_TC001) | Captcha is visible | Using three times incorrect login |
| | | [TS02_TC002](#TS02_TC002) | Captcha is visible | Using three times incorrect login, accept captcha, using one times incorrect login |
| | | [TS02_TC003](#TS02_TC003) | Captcha is visible | Using two times incorrect login, correct login and logout, usig one times incorrect login |
| [TS03](#TS03) | Check  my children functionality | | | |
| | | [TS03_TC001](#TS03_TC001) | Successful adding baby | Using pregnancy and no gender radio |
| | | [TS03_TC002](#TS03_TC002) | Successful adding baby | Using pregnancy and female radio |
| | | [TS03_TC003](#TS03_TC003) | Successful adding baby | Using pregnancy and male radio |
| | | [TS03_TC004](#TS03_TC004) | Successful adding baby | Using baby born and male radio |
| | | [TS03_TC005](#TS03_TC005) | Successful adding baby | Using baby born and female radio |
***
    

### Test Scenario TS01: Check Login Functionality <a name="TS01"></a>
    

test_TS01_TC001_successful_login_with_username: <a name="TS01_TC001"></a>
```yaml
Preconditions:
    Registered and active user in the system

Steps:
    1. Go to login page
    2. Verify by url if login page is show
    3. Try to login with correct username and password
    4. Verify by url if club page is show
    5. Click on icon account
    6. Verify logout button is visible
    7. Verify text button is "Wyloguj"
    8. Click on logout button
    9. Verify login button is visible
    10. Verify text button is "zaloguj"

Expected results: 
    Successful login with user name
```

test_TS01_TC002_successful_login_with_email: <a name="TS01_TC002"></a>
```yaml
Preconditions:
    Registered and active user in the system

Steps:
    1. Go to login page
    2. Verify by url if login page is show
    3. Try to login with correct e-mail address and password
    4. Verify by url if club page is show
    5. Click on icon account
    6. Verify text button is "Wyloguj"
    7. Click on logout button
    8. Verify text button is "zaloguj"

Expected results:
    Successful login with email
```

test_TS01_TC003_successful_login_with_email_capitalizer: <a name="TS01_TC003"></a>
```yaml
Preconditions:
    Registered and active user in the system

Steps:
    1. Go to login page
    2. Type login - correct e-mail address with big first char
    3. Type correct password
    4. Click on icon account
    5. Verify text button is "Wyloguj"

Expected results:
    Successful login with capitalizer email
```

test_TS01_TC009_successful_login_with_facebook: <a name="TS01_TC009"></a>
```yaml
Preconditions:
    Registered and active facebook user

Steps:
    1. Go to login page
    2. Click on facebook butoon
    3. Type correct "email"
    4. Type correct "password"
    5. Click on "Zaloguj" button
    6. Click on icon account
    7. Verify text link is "Moje dzieci" - in drop-down
    8. Verify URL is "klub-logged-in/moj-klub-maluszka/"

Expected results:
    Successful login with email
```

test_TS01_TC004_failed_login_correct_email_and_incorrect_password: <a name="TS01_TC004"></a>
```yaml
Preconditions:
    None

Steps: 
    1. Go to login page
    2. Verify by url if login page is show
    3. Verify text button is "zaloguj"
    4. Type login - correct e-mail address
    5. Type invalid password
    6. Click on login button
    7. Verify by url if login page is still visible
    8. Click on icon account
    9. Verify text button is "zaloguj" - in drop-down
    10. Type login - correct e-mail address
    11. Type invalid password and click on "Enter" key
    12. Click on icon account
    13. Verify text button is not "Wyloguj"

Expected results:
    Failed login
```

test_TS01_TC005_failed_login_incorrect_email_and_correct_password: <a name="TS01_TC005"></a>
```yaml
Preconditions:
    None

Steps:
    1. Go to login page
    2. Type login - incorrect e-mail address
    3. Type correct password
    4. Click on login button
    5. Click on icon account
    6. Verify text button is not "Wyloguj" - in drop-down
    7. Type login - incorrect e-mail address
    8. Type correct password and click on "Enter" key
    9. Click on icon account
    10. Verify text button is "Zaloguj" -n drop-down

Expected results:
    Failed login
```

test_TS01_TC006_failed_login_correct_email_and_password_with_space_key: <a name="TS01_TC006"></a>
```yaml
Preconditions:
    None

Steps:
    1. Go to login page
    2. Type login - space key + correct e-mail address
    3. Type password - space key + correct password
    4. Click on "Enter" key
    5. Click on icon account
    6. Verify text button is "Zaloguj"

Expected results:
    Failed login
```

test_TS01_TC007_failed_login_email_and_password_are_left_blank: <a name="TS01_TC007"></a>
```yaml
Preconditions:
    None

Steps:
    1. Go to login page
    2. Click on password input
    3. Click on "Enter" key
    4. Verify text button is "Zaloguj"
    5. Click on login button
    6. Verify by url if login page is still visible
    7. Verify text button is "Zaloguj"

Expected results:
    Failed login
```

test_TS01_TC008_failed_login_reverse_data_input: <a name="TS01_TC008"></a>
```yaml
Preconditions:
    None

Steps:
    1. Go to login page
    2. Type login - correct "passsword"
    3. Type password - correct "email"
    4. Click on "Enter" key
    5. Verify text button is "Zaloguj"

Expected results:
    Failed login
```


### Test Scenario TS02: Check captcha functionality <a name="TS02"></a>

 
test_TS02_TC001_captcha_is_visible_after_three_times_incorrect_login: <a name="TS02_TC001"></a>
```yaml
Preconditions:
    None

Steps:
    . Go to home page
    2. Click on icon account
    3. Click on logout button
    4. Verify by url if login page is show
    5. Try to login with incorrect e-mail address and password *3 [three times]
    6. Verify by url if validation page is show
    7. Try to click on captcha checkbox

Expected results:
    Captcha is visible
```

test_TS02_TC002_captcha_is_visible_again_after_one_times_incorrect_login: <a name="TS02_TC002"></a>
```yaml
Preconditions:
    None
 
Steps:
    1. Go to login page
    2. Verify by url if login page is show
    3. Try to login with incorrect e-mail address and password [only one]
    4. Verify by url if validation page is show
    5. Verify by text ['reCAPTCHA']if captcha is show
    6. Try to click on captcha checkbox

Expected results:
    Captcha is visible
```

test_TS02_TC003_captcha_is_visible_after_three_times_incorrect_login_total_quantity: <a name="TS02_TC003"></a>
```yaml
Preconditions:
    None
 
Steps:
    1. Go to login page
    2. Try to login with incorrect e-mail address and password *2 [two times]
    3. Verify text button is still "Zaloguj"
    4. Login with correct e-mail address and password
    5. Click on icon account
    6. Verify link text is "Mój profil"
    7. Click on "Wyloguj"
    8. Try to login with incorrect e-mail address and password
    9. Try to click on captcha checkbox

Expected results:
    Captcha is visible
```

### Test Scenario TS03: Check  my children functionality <a name="TS03"></a>

test_TS03_TC001_successful_adding_pregnancy_with_no_gender: <a name="TS03_TC001"></a>
```yaml
Preconditions:
     Registered, active user in the system and login
 
Steps:
    1. Go to add baby page
    2. Verify current url is '/profil-uzytkownika/dodaj-dziecko'
    3. Click on "Dodaj dziecko"
    4. Verify color of "Jestem w ciąży" == red
    5. Click on "Jestem w ciąży"
    6. Click on "Dodaj dziecko"
    7. Verify color of "Nieznana" == red
    8. Click on "Nieznana"
    9. Verify select day is clickable and set day from date(current date + 60 day)
    10. Verify select month is clickable and set month from date(current date + 60 day)
    11. Verify select year is clickable and set year from date(current date + 60 day)
    12. Verify section of registration gift is visible
    13. Click on "Dodaj dziecko"
    14. Verify current url is '/profil-uzytkownika/lista-dzieci'
    15. Verify img stork is visible
    16. Verify name is "nieznane"
    17. Verify link text is visibe = 'Potwierdź datę urodzenia dziecka'
    18. Verify date of brirth is like random_number.current_month_pus_one.current_year
    19. Verify gender is 'Nieznana'
    20. Verify gift for childbirth  is 'NIE'

Expected results:
    All test steps passed as excepted
```

test_TS03_TC002_successful_adding_pregnancy_with_female <a name="TS03_TC002"></a>
```yaml
Preconditions:
     Registered, active user in the system and login
 
Steps:
    1. Go to add baby page
    2. Verify current url is '/profil-uzytkownika/dodaj-dziecko'
    3. Click on "Dodaj dziecko"
    4. Verify color of "Jestem w ciąży" == red
    5. Click on "Jestem w ciąży"
    6. Click on "Dodaj dziecko"
    7. Verify color of "Dziewczynka" == red
    8. Click on "Dziewczynka"
    9. Verity alert 'Pole jest wymagane' is visible 
    10. Verify select day is clickable and set day = current day
    11. Verify select month is clickable and set month = current month
    12. Verify select year is clickable and set year =  current year
    13. Verify section of registration gift is visible
    14. Type random name from csv file and click Enter key
    15. Verify current url is '/profil-uzytkownika/lista-dzieci'
    16. Verify img stork is visible
    17. Verify name is enter name from no 13
    18. Verify link text is visibe = 'Potwierdź datę urodzenia dziecka'
    19. Verify date of brirth is like current_day.current_month.current_year
    20. Verify gender is 'Dziewczynka'
    21. Verify gender 'Nieznana' is not in page source 
    22. Verify gift for childbirth  is 'NIE'

Expected results:
    All test steps passed as excepted
```

test_TS03_TC003_successful_adding_pregnancy_with_male <a name="TS03_TC003"></a>
```yaml
Preconditions:
     Registered, active user in the system and login
 
Steps:
    1. Go to add baby page
    2. Verify current url is '/profil-uzytkownika/dodaj-dziecko'
    3. Click on "Dodaj dziecko"
    4. Verify color of "Jestem w ciąży" == red
    5. Click on "Jestem w ciąży"
    6. Click on "Dodaj dziecko"
    7. Verify color of "Chłopiec" == red
    8. Click on "Chłopiec"
    9. Verify alert 'Pole jest wymagane' is visible 
    10. Verify select day is clickable and set day = future day  [from (curent date + 270 day)]
    11. Verify select month is clickable and set month = future month [from (curent date + 270 day)]
    12. Verify select year is clickable and set year =  future year [from (curent date + 270 day)]
    13. Type random name from csv file 
    14. Verify section of registration gift is visible
    15. Select checkbox in registration gift section
    16. Verify name from no 13 is visible in triangle
    17. Load random town name, post code, street name, street number and phon nmber from csv files
    18. Enter data from no 16
    19. Click on "Dodaj dziecko"
    20. Verify current url is '/profil-uzytkownika/lista-dzieci'
    21. Verify alert icon and text is visible
    22. Verify img stork is visible
    23. Verify "Imię nieznane" is not in page source
    24. Verify name is the same like entered in no 13
    25. Verify name from no 13 is visible in triangle
    26. Verify text 'Potwierdź datę urodzenia dziecka' is not in page source
    27. Verify date of brirth is like no10.no11.no12
    28. Verify gender is 'Chłopiec'
    29. Verify gender 'Nieznana' is not in page source 
    30. Verify gift for childbirth  is 'TAK'

Expected results:
    All test steps passed as excepted
```

test_TS03_TC004_successful_adding_baby_born_with_male <a name="TS03_TC004"></a>
```yaml
Preconditions:
     Registered, active user in the system and login
 
Steps:
    1. Go to add baby page
    2. Verify current url is '/profil-uzytkownika/dodaj-dziecko'
    3. Click on "Dodaj dziecko"
    4. Verify color of "Mam już dziecko" == red
    5. Click on "Mam już dziecko"
    6. Click on "Dodaj dziecko"
    7. Verify color of "Chłopiec" == red
    8. Click on "Chłopiec"
    9. Verify alert 'Pole jest wymagane' is visible 
    10. Verify select day is clickable and set day = past day  [from (curent date -1095 day)]
    11. Verify select month is clickable and set month = past month [from (curent date -1095 day)]
    12. Verify select year is clickable and set year =  past year [from (curent date -1095 day)]
    13. Type random name from csv file 
    14. Click on "Dodaj dziecko"
    15. Verify current url is '/profil-uzytkownika/lista-dzieci'
    16. Verify alert icon and text is visible
    17. Verify img stork is not visible and not in page source
    18. Verify "Imię nieznane" is not in page source
    19. Verify name is visible and the same like entered in no 13
    20. Verify text 'Potwierdź datę urodzenia dziecka' is not in page source
    21. Verify date of brirth is like no10.no11.no12
    28. Verify gender is 'Chłopiec'
    29. Verify gender 'Nieznana' is not in page source 
    30. Verify gift for childbirth  is 'NIE'

Expected results:
    All test steps passed as excepted
```

test_TS03_TC005_successful_adding_baby_born_with_female <a name="TS03_TC005"></a>
```yaml
Preconditions:
     Registered, active user in the system and login
 
Steps:
    1. Go to add baby page
    2. Verify current url is '/profil-uzytkownika/dodaj-dziecko'
    3. Click on "Dodaj dziecko"
    4. Verify alert is visible and color == red
    5. Click on "Mam już dziecko"
    6. Click on "Dodaj dziecko"
    7. Verify color of "Dziewczynka" == red
    8. Click on "Dziewczynka"
    9. Verify alert 'Pole jest wymagane' is visible and is in page source 
    10. Verify select day is clickable and set day = past day  [from (curent date -47 day)]
    11. Verify select month is clickable and set month = past month [from (curent date -47 day)]
    12. Verify select year is clickable and set year =  past year [from (curent date -47 day)]
    13. Verify section of registration gift is not visible
    14. Verify select day is clickable and set day = past day  [from (curent date -46 day)]
    15. Verify select month is clickable and set month = past month [from (curent date -46 day)]
    16. Verify select year is clickable and set year =  past year [from (curent date -46 day)]
    17. Verify section of registration gift is visible
    18. Select checkbox in registration gift section
    19. Enter random name from csv file
    20. Load random town name, post code, street name, street number and phon number from csv files and enter data
    21. Verify name from no 19 is visible in triangle
    22. Click on "Dodaj dziecko"
    23. Verify current url is '/profil-uzytkownika/lista-dzieci'
    24. Verify alert icon and text is visible
    25. Verify img stork is not visible and not in page source
    26. Verify "Imię nieznane" is not in page source
    27. Verify name is visible and the same like entered in no 19
    28. Verify name from no 16 is visible in triangle
    29. Verify date of brirth is like no14.no15.no16
    30. Verify gender is 'Dziewczyna'
    31. Verify gender 'Nieznana' is not in page source 
    32. Verify gift for childbirth  is 'TAK'

Expected results:
    All test steps passed as excepted
```

