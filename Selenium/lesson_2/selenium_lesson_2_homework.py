from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestSuite:

    def __init__(self, url, driver):
        self.__url = url
        self.__driver = driver

    def get_url(self):
        return self.__url

    def get_driver(self):
        return self.__driver

    def tear_down(self):
        self.__driver.close()

    def test_valid_data(self):
        try:
            self.get_driver().get(self.get_url())
            self.get_driver().maximize_window()
            time.sleep(2)

            full_name_field = self.get_driver().find_element(By.ID, "userName")
            full_name_field.send_keys("Бугаев Дмитрий")

            email_field = self.get_driver().find_element(By.ID, "userEmail")
            email_field.send_keys("bugaev_d@example.com")

            current_address_field = self.get_driver().find_element(By.ID, "currentAddress")
            current_address_field.send_keys("Санкт-Петербург, Невский проспект, д.151")

            permanent_address_field = self.get_driver().find_element(By.ID, "permanentAddress")
            permanent_address_field.send_keys("Санкт-Петербург, Проспект Большевиков, д.32")

            submit_button = self.get_driver().find_element(By.ID, "submit")
            submit_button.click()

            time.sleep(2)

            result_box = self.get_driver().find_element(By.ID, "output")

            assert "Бугаев Дмитрий" in result_box.text
            assert "bugaev_d@example.com" in result_box.text
            assert "Санкт-Петербург, Невский проспект, д.151" in result_box.text
            assert "Санкт-Петербург, Проспект Большевиков, д.32" in result_box.text
            print("Тест успешно пройден!")

        finally:
            print("Очищаем driver между тестами для чистоты эксперимента.")

    def test_empty_fields(self):
        try:
            self.get_driver().get(self.get_url())
            self.get_driver().maximize_window()
            time.sleep(2)

            submit_button = self.get_driver().find_element(By.ID, "submit")
            submit_button.click()

            time.sleep(2)

            result_box = self.get_driver().find_element(By.ID, "output")

            assert len(result_box.text) == 0
            print("Тест пройден")
        finally:
            print("Очищаем driver между тестами для чистоты эксперимента.")


    def test_invalid_email(self):
        try:
            self.get_driver().get(self.get_url())
            self.get_driver().maximize_window()
            time.sleep(2)

            full_name_field = self.get_driver().find_element(By.ID, "userName")
            full_name_field.send_keys("Бугаев Дмитрий")

            email_field = self.get_driver().find_element(By.ID, "userEmail")
            email_field.send_keys("bugaev_dexample.com")

            current_address_field = self.get_driver().find_element(By.ID, "currentAddress")
            current_address_field.send_keys("Санкт-Петербург, Невский проспект, д.151")

            permanent_address_field = self.get_driver().find_element(By.ID, "permanentAddress")
            permanent_address_field.send_keys("Санкт-Петербург, Проспект Большевиков, д.32")

            submit_button = self.get_driver().find_element(By.ID, "submit")
            submit_button.click()

            time.sleep(2)

            result_box = self.get_driver().find_element(By.ID, "output")

            assert "bugaev_dexample.com" not in result_box.text
            print("Тест пройден успешно!")
        finally:
            print("Очищаем driver между тестами для чистоты эксперимента.")

    def test_long_email(self):
        try:
            self.get_driver().get(self.get_url())
            self.get_driver().maximize_window()
            time.sleep(2)

            full_name_field = self.get_driver().find_element(By.ID, "userName")
            full_name_field.send_keys("Бугаев Дмитрий")

            email_field = self.get_driver().find_element(By.ID, "userEmail")
            email_field.send_keys("bugaev_d" * 20 + "@example.com")

            current_address_field = self.get_driver().find_element(By.ID, "currentAddress")
            current_address_field.send_keys("Санкт-Петербург, Невский проспект, д.151")

            permanent_address_field = self.get_driver().find_element(By.ID, "permanentAddress")
            permanent_address_field.send_keys("Санкт-Петербург, Проспект Большевиков, д.32")

            submit_button = self.get_driver().find_element(By.ID, "submit")
            submit_button.click()

            time.sleep(2)

            result_box = self.get_driver().find_element(By.ID, "output")

            assert len(result_box.text) == 0
            print("Тест пройден")

        finally:
            print("Очищаем driver между тестами для чистоты эксперимента.")

text_box = TestSuite("https://qa-guru.github.io/one-page-form/text-box.html", webdriver.Chrome())
text_box.test_valid_data()
text_box.test_empty_fields()
text_box.test_invalid_email()
text_box.test_long_email()
text_box.tear_down()