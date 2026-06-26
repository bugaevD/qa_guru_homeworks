import pytest
import allure
from selenium import webdriver

from login_form_page import LoginForm, LoginData


@allure.epic("Тестирование формы логина")
@allure.feature("Форма логина")
class TestLoginForm:
    @pytest.fixture
    def driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-extensions')
        with allure.step("Инициализируем браузер Chrome"):
            driver = webdriver.Chrome(options=chrome_options)
        yield driver
        with allure.step("Закрываем браузер Chrome"):
            driver.quit()

    @pytest.fixture
    def login_form_page(self, driver):
        with allure.step("Создаем объект формы логина, открываем форму логина"):
            login_form_page = LoginForm(driver)
            login_form_page.open_login_page()
        return login_form_page

    @allure.story("Позитивный сценарий")
    @allure.title("Корректный логин и пароль")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_positive_data(self, login_form_page):
        with allure.step("Подготавливаем тестовые данные"):
            login_data = LoginData(username="user1", password="password1")
            allure.attach(
                f"Логин: {login_data.username}, Пароль: {login_data.password}",
                name="Тестовые данные",
                attachment_type=allure.attachment_type.TEXT
            )
        with allure.step("Заполняем форму"):
            login_form_page.fill_login_form(login_data)
            allure.attach(
                login_form_page.driver.get_screenshot_as_png(),
                name="Успешный вход",
                attachment_type=allure.attachment_type.PNG
            )
        with allure.step("Проверяем вход в систему"):
            login_form_page.assert_positive_login(login_data)

    @pytest.mark.parametrize("username, password, expected_error, test_name", [
        ("user2", "password1", "Wrong login or password", "Некорректный логин"),
        ("user1", "password2", "Wrong login or password", "Некорретный пароль"),
        ("", "", "Login and password are required (minimum 3 and 6 characters)", "Пустые поля"),
        ("", "password1", "Login is required (minimum 3 characters)", "Пустое поле логина"),
        ("user1", "", "Password is required (minimum 6 characters)", "Пустое поле пароля")
    ])
    @allure.story("Негативный сценарий")
    @allure.title("Некорректный логин")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.negative
    def test_negative_data(self, login_form_page, username, password, expected_error, test_name):
        with allure.step("Подготавливаем тестовые данные"):
            allure.dynamic.title(f"Негативный сценарий: {test_name}")
            login_data = LoginData(username=username, password=password)
            allure.attach(
                f"Логин: {login_data.username}, Пароль: {login_data.password}",
                name="Тестовые данные",
                attachment_type=allure.attachment_type.TEXT
            )
        with allure.step("Заполняем форму"):
            login_form_page.fill_login_form(login_data)
            allure.attach(
                login_form_page.driver.get_screenshot_as_png(),
                name="Скриншот ошибки",
                attachment_type=allure.attachment_type.PNG
            )
        with allure.step("Проверяем сообщение об ошибке"):
            error_message = login_form_page.get_error_message()

            assert error_message == expected_error, f"Ожидали ошибку: {expected_error}, получили: {error_message}"
