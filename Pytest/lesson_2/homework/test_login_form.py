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

    @allure.story("Негативный сценарий")
    @allure.title("Некорректный логин")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.negative
    def test_invalid_login(self, login_form_page):
        with allure.step("Подготавливаем тестовые данные с некорректным логином"):
            login_data = LoginData(username="user2", password="password1")
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
                attachment_type=allure.attachment_type.PNG)
        with allure.step("Проверка сообщения об ошибке"):
            login_form_page.assert_wrong_login()

    @allure.story("Негативный сценарий")
    @allure.title("Некорректный пароль")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.negative
    def test_invalid_password(self, login_form_page):
        with allure.step("Подготавливаем тестовые данные с некорректным паролем"):
            login_data = LoginData(username="user1", password="password2")
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
        with allure.step("Проверка сообщения об ошибке"):
            login_form_page.assert_wrong_login()
    @allure.story("Негативный сценарий")
    @allure.title("Пустые поля")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.negative
    def test_empty_fields(self, login_form_page):
        with allure.step("Подготавливаем пустые тестовые данные"):
            login_data = LoginData()
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
        with allure.step("Проверка сообщения об ошибке"):
            login_form_page.assert_empty_fields()

    @allure.story("Негативный сценарий")
    @allure.title("Пустое поле логина")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.negative
    def test_empty_login(self, login_form_page):
        with allure.step("Подготавливаем тестовые данные с пустым логином"):
            login_data = LoginData(password="password1")
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
        with allure.step("Проверка сообщения об ошибке"):
            login_form_page.assert_empty_login()

    @allure.story("Негативный сценарий")
    @allure.title("Пустое поле пароля")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.negative
    def test_empty_password(self, login_form_page):
        with allure.step("Подготавливаем тестовые данные с пустым паролем"):
            login_data = LoginData(username="user1")
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
        with allure.step("Проверка сообщения об ошибке"):
            login_form_page.assert_empty_password()
