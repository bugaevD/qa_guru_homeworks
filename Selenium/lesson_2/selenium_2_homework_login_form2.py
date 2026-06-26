from selenium import webdriver
from selenium.webdriver.common.by import By


class LoginForm:
    LOGIN_FIELD = (By.ID, "login-input")
    PASSWORD_FIELD = (By.ID, "password-input")
    LOGIN_BUTTON = (By.ID, "submit-button")
    LOGOUT_BUTTON = (By.ID, "logout-button")
    WELCOME_MESSAGE = (By.ID, "welcome-message")
    ERROR_MESSAGE = (By.ID, "error-message")

    def __init__(self, url):
        self.driver = None
        self.url = url

    def tear_up(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.maximize_window()

    def tear_down(self):
        self.driver.quit()

    def field_login(self, login):
        self.driver.find_element(*self.LOGIN_FIELD).send_keys(login)

    def field_password(self, password):
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)

    def login_button(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def logout_button(self):
        self.driver.find_element(*self.LOGOUT_BUTTON).click()

    def welcome_message_text(self):
        return self.driver.find_element(*self.WELCOME_MESSAGE).text

    def error_message_text(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text


def test_valid_data_login():
    login_form = LoginForm(url="https://qa-guru.github.io/one-page-form/login.html")

    login_form.tear_up()
    login_form.field_login("user1")
    login_form.field_password("password1")
    login_form.login_button()

    assert login_form.welcome_message_text() == "Welcome, user1!"

    login_form.tear_down()


def test_empty_fields():
    login_form = LoginForm(url="https://qa-guru.github.io/one-page-form/login.html")

    login_form.tear_up()
    login_form.login_button()

    assert login_form.error_message_text() == "Login and password are required (minimum 3 and 6 characters)"

    login_form.tear_down()


def test_invalid_login():
    login_form = LoginForm(url="https://qa-guru.github.io/one-page-form/login.html")

    login_form.tear_up()
    login_form.field_login("user2")
    login_form.field_password("password1")
    login_form.login_button()

    assert login_form.error_message_text() == "Wrong login or password"

    login_form.tear_down()


def test_invalid_password():
    login_form = LoginForm(url="https://qa-guru.github.io/one-page-form/login.html")

    login_form.tear_up()
    login_form.field_login("user1")
    login_form.field_password("password2")
    login_form.login_button()

    assert login_form.error_message_text() == "Wrong login or password"

    login_form.tear_down()
