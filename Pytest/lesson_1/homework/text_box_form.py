from dataclasses import dataclass

from selenium.webdriver.support.wait import WebDriverWait
from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.support import expected_conditions as ec


@dataclass
class UserData:
    name: str | None = None
    email: str | None = None
    current_address: str | None = None
    permanent_address: str | None = None


@dataclass
class OutputData:
    name: str | None = None
    email: str | None = None
    current_address: str | None = None
    permanent_address: str | None = None


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

    def fill_full_name(self, full_name=None):
        if full_name:
            self.full_name_input.send_keys(full_name)

    def fill_email(self, email=None):
        if email:
            self.email_input.send_keys(email)

    def click_button(self):
        self.submit_button.click()

    def fill_current_address(self, current_address=None):
        if current_address:
            self.current_address_input.send_keys(current_address)

    def fill_permanent_address(self, permanent_address=None):
        if permanent_address:
            self.permanent_address_input.send_keys(permanent_address)

    def fill_full_form(self, user_data: UserData):
        self.fill_full_name(user_data.name)
        self.fill_email(user_data.email)
        self.fill_current_address(user_data.current_address)
        self.fill_permanent_address(user_data.permanent_address)
        self.click_button()

    def get_output_data(self):
        self.wait.until(ec.visibility_of(self.output_data))
        output_data = OutputData(
            name=self.output_name.text.replace("Name:", "").strip(),
            email=self.output_email.text.replace("Email:", "").strip(),
            current_address=self.output_cur_adr.text.replace("Current Address :", "").strip(),
            permanent_address=self.output_per_adr.text.replace("Permananet Address :", "").strip()
        )

        return output_data

    def assert_valid_result(self, user_data: UserData):
        actual_data = self.get_output_data()

        if user_data.name:
            assert actual_data.name == user_data.name.strip()
        if user_data.email:
            assert actual_data.email == user_data.email.strip()
        if user_data.current_address:
            assert actual_data.current_address == user_data.current_address.strip()
        if user_data.permanent_address:
            assert actual_data.permanent_address == user_data.permanent_address.strip()

    def assert_invalid_email(self, user_data: UserData, expected_error_message=None):
        email_error = self.get_validation_message()
        if user_data.email:
            assert len(email_error.strip()) > 0, "Форма пропустила невалидный email!"
        if expected_error_message:
            assert email_error == expected_error_message, f"Ожидаемое сообщение об ошибке: {expected_error_message}, не совпадает с полученным: {email_error}"

    def assert_long_data(self):
        assert not self.output_data.is_displayed(), "Форма пропустила длинное поле!"

    def assert_empty_fields(self):
        assert not self.output_data.is_displayed(), "Форма отправилась с пустыми полями!"

    def assert_security_payload(self, user_data: UserData):
        actual_data = self.get_output_data()
        assert actual_data is not None, "Форма упала при вводе небезопасных значений!"
        if user_data.name:
            assert actual_data.name == user_data.name.strip(), "Введенные данные не совпадают!"
