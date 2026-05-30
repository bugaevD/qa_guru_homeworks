import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

def test_valid_data():
    try:
        driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
        driver.maximize_window()
        time.sleep(2)

        full_name_field = driver.find_element(By.ID, "userName")
        full_name_field.send_keys("Бугаев Дмитрий")

        email_field = driver.find_element(By.ID, "userEmail")
        email_field.send_keys("bugaev_d@example.com")

        current_address_field = driver.find_element(By.ID, "currentAddress")
        current_address_field.send_keys("Санкт-Петербург, Невский проспект, д.151")

        permanent_address_field = driver.find_element(By.ID, "permanentAddress")
        permanent_address_field.send_keys("Санкт-Петербург, Проспект Большевиков, д.32")

        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        time.sleep(2)

        result_box = driver.find_element(By.ID, "output")

        assert "Бугаев Дмитрий" in result_box.text
        assert "bugaev_d@example.com" in result_box.text
        assert "Санкт-Петербург, Невский проспект, д.151" in result_box.text
        assert "Санкт-Петербург, Проспект Большевиков, д.32" in result_box.text
        print("Тест успешно пройден!")

    finally:
        driver.quit()

