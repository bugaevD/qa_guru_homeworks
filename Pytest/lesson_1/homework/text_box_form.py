from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.support import expected_conditions as ec


class TextBoxForm(PageFactory):
    URL = "https://qa-guru.github.io/one-page-form/text-box.html"

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)
        self.locators = {
            "full_name_input": ("ID", "userName"),
            "email_input": ("ID", "userEmail"),
            "current_address_input": ("ID", "currentAddress"),
            "permanent_address_input": ("ID", "permanentAddress"),
            "submit_button": ("ID", "submit"),
            "output_data": ("ID", "output"),
            "output_name": ("XPATH", "//p[@id='name']"),
            "output_email": ("XPATH", "//p[@id='email']"),
            "output_cur_adr": ("XPATH", "//p[@id='currentAddress']"),
            "output_per_adr": ("XPATH", "//p[@id='permanentAddress']"),

        }

    def open_text_box_page(self):
        self.driver.get(self.URL)

    def tear_down(self):
        self.driver.quit()

    def get_validation_message(self):
        validation_message = self.email_input.get_attribute("validationMessage")
        return validation_message

    def fill_full_form(self, full_name=None, email=None, current_address=None, permanent_address=None):
        if full_name is not None:
            self.full_name_input.send_keys(full_name)
        if email is not None:
            self.email_input.send_keys(email)
        if current_address is not None:
            self.current_address_input.send_keys(current_address)
        if permanent_address is not None:
            self.permanent_address_input.send_keys(permanent_address)

        self.submit_button.click()

    def get_output_data(self):
        self.wait.until(ec.visibility_of(self.output_data))
        full_name = self.output_name.text.replace("Name:", "").strip()
        email = self.output_email.text.replace("Email:", "").strip()
        current_address = self.output_cur_adr.text.replace("Current Address :", "").strip()
        permanent_address = self.output_per_adr.text.replace("Permananet Address :", "").strip()

        return {"full_name": full_name, "email": email, "current_address": current_address,
                "permanent_address": permanent_address}

    def assert_valid_result(self, full_name=None, email=None, current_address=None, permanent_address=None):
        actual_data = self.get_output_data()

        if full_name is not None:
            assert actual_data["full_name"] == full_name.strip(), "Введенные данные не совпадают!"
        if email is not None:
            assert actual_data["email"] == email.strip(), "Введенные данные не совпадают!"
        if current_address is not None:
            assert actual_data["current_address"] == current_address.strip(), "Введенные данные не совпадают!"
        if permanent_address is not None:
            assert actual_data["permanent_address"] == permanent_address.strip(), "Введенные данные не совпадают!"

    def assert_invalid_email(self, email=None, error_message=None):
        email_error = self.get_validation_message()
        if email is not None:
            assert len(email_error.strip()) > 0, "Форма пропустила невалидный email!"

    def assert_long_data(self):
        assert not self.output_data.is_displayed(), "Форма пропустила длинное поле!"

    def assert_empty_fields(self):
        assert not self.output_data.is_displayed(), "Форма отправилась с пустыми полями!"

    def assert_security_payload(self, security_payload):
        actual_data = self.get_output_data()
        assert actual_data is not None, "Форма упала при вводе небезопасных значений!"
        assert actual_data["full_name"] == security_payload.strip(), "Введенные данные не совпадают!"
