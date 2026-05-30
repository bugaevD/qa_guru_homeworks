import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

def set_up_test(driver):
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
    driver = webdriver.Chrome()
    driver.maximize_window()

def tear_down_test(driver):
    driver.quit()

full_name_locator = "userName"
email_locator = "userEmail"
submit_locator = "submit"
result_box_locator = "output"

def test01():

    print("Рефакторинг")

    driver = webdriver.Chrome()

    try:
        set_up_test(driver)
        time.sleep(3)

        full_name_field = driver.find_element(By.ID, full_name_locator)
        full_name_field.send_keys("Иван Иванов")

        email_field = driver.find_element(By.ID, email_locator)
        email_field.send_keys("ivan@example.com")

        submit_button = driver.find_element(By.ID, submit_locator)
        submit_button.click()

        time.sleep(3)

        result_box = driver.find_element(By.ID, result_box_locator)

        # Проверяем, что в блоке результата появился введенный текст
        assert "Иван Иванов" in result_box.text
        print("Тест успешно пройден!")

    finally:
        # 5. Закрытие браузера в любом случае
        tear_down_test(driver)


def test02():
    print("Рефакторинг, вторая итерация")

    driver = webdriver.Chrome()

    try:
        set_up_test(driver)
        time.sleep(3)

        full_name_field = driver.find_element(By.ID, full_name_locator)
        full_name_field.send_keys("Иван Иванов")

        email_field = driver.find_element(By.ID, email_locator)
        email_field.send_keys("ivanexample.com")

        submit_button = driver.find_element(By.ID, submit_locator)
        submit_button.click()

        time.sleep(3)

        result_box = driver.find_element(By.ID, result_box_locator)

        # Проверяем, что в блоке результата появился введенный текст
        assert "Иван Иванов" in result_box.text
        print("Тест успешно пройден!")

    finally:
        # 5. Закрытие браузера в любом случае
        tear_down_test(driver)