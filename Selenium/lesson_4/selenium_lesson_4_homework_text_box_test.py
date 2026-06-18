from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class TestSuite:
    URL = "https://qa-guru.github.io/one-page-form/text-box.html"

    FULL_NAME = (By.ID, "userName")
    EMAIL = (By.ID, "userEmail")
    CURRENT_ADDRESS = (By.ID, "currentAddress")
    PERMANENT_ADDRESS = (By.ID, "permanentAddress")
    SUBMIT_BUTTON = (By.ID, "submit")
    OUTPUT = (By.ID, "output")
    FULL_NAME_OUTPUT = (By.ID, "name")
    EMAIL_OUTPUT = (By.ID, "email")
    CUR_ADDR_OUTPUT = ("xpath", "//div[@id='output']/p[@id='currentAddress']")
    PER_ADDR_OUTPUT = ("xpath",
                       "//div[@id='output']/p[@id='permanentAddress']")

    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.URL)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)

    def tear_down(self):
        self.driver.quit()

    def fill_full_name(self, full_name):
        self.driver.find_element(*self.FULL_NAME).send_keys(full_name)

    def fill_email(self, email):
        self.driver.find_element(*self.EMAIL).send_keys(email)

    def fill_current_address(self, current_address):
        self.driver.find_element(*self.CURRENT_ADDRESS).send_keys(current_address)

    def fill_permanent_address(self, permanent_address):
        self.driver.find_element(*self.PERMANENT_ADDRESS).send_keys(permanent_address)

    def get_output_data(self):
        self.wait.until(ec.visibility_of_element_located((By.ID, "output")))

        name = self.driver.find_element(*self.FULL_NAME_OUTPUT).text.replace("Name:", "")
        email = self.driver.find_element(*self.EMAIL_OUTPUT).text.replace("Email:", "")
        current_address = self.driver.find_element(*self.CUR_ADDR_OUTPUT).text.replace(
            "Current Address :", "")
        permanent_address = self.driver.find_element(*self.PER_ADDR_OUTPUT).text.replace(
            "Permananet Address :", "")

        return {"name": name, "email": email, "current_address": current_address,
                "permanent_address": permanent_address}

    def click_submit_button(self):
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def get_validation_message(self):
        validation_message_input = self.driver.find_element(*self.EMAIL)
        validation_message = validation_message_input.get_attribute("validationMessage")
        return validation_message

    def test_valid_data(self):

        full_name = "Bugaev Dmitry"
        email = "bugaev1@example.com"
        current_address = "Санкт-Петербург, Невский проспект, д.151"
        permanent_address = "Санкт-Петербург, Проспект Большевиков, д.32"

        try:
            self.setup()
            self.fill_full_name(full_name)
            self.fill_email(email)
            self.fill_current_address(current_address)
            self.fill_permanent_address(permanent_address)
            self.click_submit_button()

            output_data = self.get_output_data()

            assert full_name == output_data["name"]
            assert email == output_data["email"]
            assert current_address == output_data["current_address"]
            assert permanent_address == output_data["permanent_address"]
            print("Все введенные данные совпадают!")

        finally:
            self.tear_down()

    def test_empty_fields(self):
        try:

            self.setup()
            self.click_submit_button()

            output_data = self.get_output_data()

            assert "" == output_data["name"]
            assert "" == output_data["email"]
            assert "" == output_data["current_address"]
            assert "" == output_data["permanent_address"]

        finally:
            self.tear_down()

    def test_invalid_email(self):
        try:
            full_name = "Bugaev Dmitry"
            email = "bugaevexample.com"
            current_address = "Санкт-Петербург, Невский проспект, д.151"
            permanent_address = "Санкт-Петербург, Проспект Большевиков, д.32"

            self.setup()
            self.fill_full_name(full_name)
            self.fill_email(email)
            self.fill_current_address(current_address)
            self.fill_permanent_address(permanent_address)
            self.click_submit_button()
            validation_massage = self.get_validation_message()

            assert validation_massage == f'Адрес электронной почты должен содержать символ "@". В адресе "{email}" отсутствует символ "@".'

        finally:
            self.tear_down()

    #
    def test_long_email(self):
        try:
            full_name = "Bugaev Dmitry"
            email = "bugaev_d" * 20 + "@example.com"
            current_address = "Санкт-Петербург, Невский проспект, д.151"
            permanent_address = "Санкт-Петербург, Проспект Большевиков, д.32"

            self.setup()
            self.fill_full_name(full_name)
            self.fill_email(email)
            self.fill_current_address(current_address)
            self.fill_permanent_address(permanent_address)
            self.click_submit_button()
            validation_massage = self.get_validation_message()

            assert len(validation_massage) > 0, "Система приняла очень длинный email"


        finally:
            self.tear_down()
