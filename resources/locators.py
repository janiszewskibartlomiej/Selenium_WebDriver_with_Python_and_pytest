from selenium.webdriver.common.by import By


class LoginPageLocators:
    ICON_ACCOUNT = (By.XPATH, "//span[contains(@class,'kkicon kkicon-account')]")
    MY_CHILDREN_LINK_TEXT = (By.XPATH, "//a[contains(text(),'Moje')]")
    DROP_DOWN_SECTION = (By.XPATH, "//div[@id='header-account']")
    USERNAME_FIELD = (By.XPATH, "//input[@placeholder='Login']")
    PASSWORD_FIELD = (By.XPATH, "//input[@placeholder='Hasło']")
    SUBMIT_BTN = (By.NAME, 'login')
    CAPTCHA_SECTION = (By.XPATH, "//div[@class='g-recaptcha']")
    LOGOUT_BUTTON = (By.LINK_TEXT, "Wyloguj")
    MY_PROFILE = (By.XPATH, "//a[contains(text(),'Mój')]")
    LOGIN_BY_FACEBOOK = (By.XPATH, "//a[@class='loginBtn--facebook']")
    FACEBOOK_EMAIL = (By.XPATH, "//input[@id='email']")
    FACEBOOK_PASSWORD = (By.XPATH, "//input[@id='pass']")
    FACEBOOK_LOGIN_BTN = (By.XPATH, "//button[@id='loginbutton']")
    ALERT_MESSAGE = (By.XPATH, "//ul[@class='errorsMessages']")


class HomePageLocators:
    ICON_ACCOUNT = (By.XPATH, "//a[@class='skip-link skip-account']")
    LOGIN_BUTTON = (By.XPATH, "//a[@class='btn btn--brand']")


class AddBabyLocators:
    I_AM_PREGNANT = (By.XPATH, "//label[@for='notBornChild']")
    I_HAVE_BABY = (By.XPATH, "//label[@for='bornChild']")
    FEMALE = (By.XPATH, "//label[@for='childNotBornGenderF']")
    MALE = (By.XPATH, "//label[@for='childNotBornGenderM']")
    NO_GENDER_RADIO = (By.XPATH, "//label[@for='childNotBornGenderNone']")
    PREGNANT_DAY = (By.XPATH, "//select[@name='borndate_[day]']")
    PREGNANT_MONTH = (By.XPATH, "//select[@name='borndate_[month]']")
    PREGNANT_YEAR = (By.XPATH, "//select[@name='borndate_[year]']")
    BORN_DAY = (By.XPATH, "//select[@name='birthdate_[day]']")
    BORN_MONTH = (By.XPATH, "//select[@name='birthdate_[month]']")
    BORN_YEAR = (By.XPATH, "//select[@name='birthdate_[year]']")
    FIRST_NAME_INPUT = (By.XPATH, "//input[@data-placeholder-born='Imię']")
    ADD_BABY_BUTTON = (By.NAME, "submit")
    ALERT_MESSAGE = (By.XPATH, "//li[@class='parsley-required']/p")
    CHECKBOX_GIFT_TEXT = (By.XPATH, "//div[@class='triangle-create']//p[1]")
    SECTION_OF_REGISTRATION_GIFT = (By.XPATH, "//div[@class='form-group registrationGiftsWrapper']")
    TOWN_NAME = (By.ID, "autocomplete-city")
    STREET_NAME = (By.ID, "autocomplete-street")
    NUMBER_OF_STREET = (By.ID, "autocomplete-zip")
    POST_CODE = (By.ID, "complete-zip")
    PHONE_NUMBER = (By.XPATH, "//input[@data-fmask='000 000 000']")
    NAME_IN_TRIANGLE = (By.XPATH, "//span[@class='triangle-childname']")


class ListOfChildrenLocators:
    IMG_STORK = (By.XPATH, "//img[@alt='Ciąża']")
    FIRST_NAME_RENDER = (By.XPATH, "//div[@class='mb-3']/h2")
    CONFIRM_DATE_OF_BIRTH_LINK = (By.LINK_TEXT, "Potwierdź datę urodzenia dziecka")
    DATE_OF_BIRTH_REGULAR = (By.XPATH, "//span[@class='font-weight-regular']")
    DATE_OF_BIRTH_BOLD = (By.XPATH, "//span[@class='font-weight-bold']")
    GENDER_SECTION = (By.XPATH, "//div[@class='mb-3']/div[contains(text(),'Płeć:')]")
    GIFT_FOR_CHILDBIRTH_INFO = (By.XPATH, "//div[@class='mb-3']/div[contains(text(),'Paczka Narodzin')]")
    NAME_IN_TRIANGLE = (By.XPATH, "//span[@class='triangle-childname']")
    ALERT_ICON = (By.XPATH, "//span[@class='alert-icon']")
    ALERT_CONTENT = (By.XPATH, "//div[@class='alert-content']")
