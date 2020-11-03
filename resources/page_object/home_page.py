from resources.page_object.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, driver, base_url):
        super().__init__(driver)

        self.driver = driver
        self.base_url = base_url

        self.driver.get(self.base_url)
