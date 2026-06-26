from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


@dataclass
class LoginData:
    username: str | None = None
    password: str | None = None


class LoginForm:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.url = "https://qa-guru.github.io/one-page-form/login.html"

    LOGIN_INPUT = (By.ID, "login-input")
    PASSWORD_INPUT = (By.ID, "password-input")
    LOGIN_BUTTON = (By.ID, "submit-button")
    ERROR_MESSAGE = (By.ID, "error-message")
    SUCCESS_PANEL = (By.ID, "success-panel")
    WELCOME_MESSAGE = (By.ID, "welcome-message")

    def setup(self):
        self.driver.get(self.url)

    def open_login_page(self):
        self.driver.get(self.url)

    def fill_login_field(self, username=None):
        if username is None:
            return
        self.driver.find_element(*self.LOGIN_INPUT).send_keys(username)

    def fill_password_field(self, password=None):
        if password is None:
            return
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def click_login_button(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def fill_login_form(self, login: LoginData):
        self.fill_login_field(login.username)
        self.fill_password_field(login.password)
        self.click_login_button()

    def get_error_message(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text

    def get_welcome_message(self):
        return self.driver.find_element(*self.WELCOME_MESSAGE).text

    def assert_positive_login(self, login: LoginData):
        success_panel = self.wait.until(ec.visibility_of_element_located(self.SUCCESS_PANEL))
        assert success_panel.is_displayed(), "Окно с приветствием не отобразилось!"

        assert self.get_welcome_message() == f"Welcome, {login.username}!"
