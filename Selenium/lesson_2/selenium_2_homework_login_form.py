from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class LoginForm:

    LOGIN_FIELD = (By.ID, "login-input")
    PASSWORD_FIELD = (By.ID, "password-input")
    LOGIN_BUTTON = (By.ID, "submit-button")
    LOGOUT_BUTTON = (By.ID, "logout-button")
    WELCOME_MESSAGE = (By.ID, "welcome-message")
    ERROR_MESSAGE = (By.ID, "error-message")


    def __init__(self, url, driver):
        self.__url = url
        self.__driver = driver

    def get_url(self):
        return self.__url

    def get_driver(self):
        return self.__driver

    def set_driver(self, driver):
        self.__driver = driver

    def tear_up(self):
        self.get_driver().get(self.get_url())
        self.get_driver().maximize_window()
        # time.sleep(2)

    def tear_down(self):
        self.get_driver().quit()

    def test_valid_login(self):
        self.tear_up()

        self.get_driver().find_element(*self.LOGIN_FIELD).send_keys("user1")
        self.get_driver().find_element(*self.PASSWORD_FIELD).send_keys("password1")
        self.get_driver().find_element(*self.LOGIN_BUTTON).click()
        welcome_message = self.get_driver().find_element(*self.WELCOME_MESSAGE).text

        assert welcome_message == "Welcome, user1!"

        self.get_driver().find_element(*self.LOGOUT_BUTTON).click()


    def test_empty_field(self):
        self.tear_up()

        self.get_driver().find_element(*self.LOGIN_BUTTON).click()
        error_message = self.get_driver().find_element(*self.ERROR_MESSAGE).text

        assert error_message == "Login and password are required (minimum 3 and 6 characters)"

    def test_invalid_login(self):
        self.tear_up()

        self.get_driver().find_element(*self.LOGIN_FIELD).send_keys("user2")
        self.get_driver().find_element(*self.PASSWORD_FIELD).send_keys("password1")
        self.get_driver().find_element(*self.LOGIN_BUTTON).click()
        error_message = self.get_driver().find_element(*self.ERROR_MESSAGE).text

        assert error_message == "Wrong login or password"

    def test_invalid_password(self):
        self.tear_up()

        self.get_driver().find_element(*self.LOGIN_FIELD).send_keys("user1")
        self.get_driver().find_element(*self.PASSWORD_FIELD).send_keys("password2")
        self.get_driver().find_element(*self.LOGIN_BUTTON).click()
        error_message = self.get_driver().find_element(*self.ERROR_MESSAGE).text

        assert error_message == "Wrong login or password"

    def test_short_login(self):
        self.tear_up()

        self.get_driver().find_element(*self.LOGIN_FIELD).send_keys("us")
        self.get_driver().find_element(*self.PASSWORD_FIELD).send_keys("password1")
        self.get_driver().find_element(*self.LOGIN_BUTTON).click()
        error_message = self.get_driver().find_element(*self.ERROR_MESSAGE).text

        assert error_message == "Login must be at least 3 characters"

    def test_short_password(self):
        self.tear_up()

        self.get_driver().find_element(*self.LOGIN_FIELD).send_keys("user1")
        self.get_driver().find_element(*self.PASSWORD_FIELD).send_keys("pass")
        self.get_driver().find_element(*self.LOGIN_BUTTON).click()
        error_message = self.get_driver().find_element(*self.ERROR_MESSAGE).text

        assert error_message == "Password must be at least 6 characters"



login_form = LoginForm("https://qa-guru.github.io/one-page-form/login.html", webdriver.Chrome())
login_form.test_valid_login()
login_form.test_empty_field()
login_form.test_invalid_login()
login_form.test_invalid_password()
login_form.test_short_login()
login_form.test_short_password()
login_form.tear_down()
