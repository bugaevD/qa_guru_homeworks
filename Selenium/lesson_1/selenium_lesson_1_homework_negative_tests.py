import time

from _pytest import assertion
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

def test_empty_fields():
    try:
        driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
        driver.maximize_window()
        time.sleep(2)

        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        time.sleep(2)

        result_box = driver.find_element(By.ID, "output")

        if len(result_box.text) > 0:
            print("Тест не пройден")
        else:
            print("Тест пройден")
    finally:
        driver.quit()

def test_invalid_email():
    try:
        driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
        driver.maximize_window()
        time.sleep(2)

        full_name_field = driver.find_element(By.ID, "userName")
        full_name_field.send_keys("Бугаев Дмитрий")

        email_field = driver.find_element(By.ID, "userEmail")
        email_field.send_keys("bugaev_dexample.com")

        current_address_field = driver.find_element(By.ID, "currentAddress")
        current_address_field.send_keys("Санкт-Петербург, Невский проспект, д.151")

        permanent_address_field = driver.find_element(By.ID, "permanentAddress")
        permanent_address_field.send_keys("Санкт-Петербург, Проспект Большевиков, д.32")

        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        time.sleep(2)

        result_box = driver.find_element(By.ID, "output")

        assert "bugaev_dexample.com" not in result_box.text
        print("Тест пройден успешно!")
    finally:
        driver.quit()

def test_long_email():
    try:
        driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
        driver.maximize_window()
        time.sleep(2)

        full_name_field = driver.find_element(By.ID, "userName")
        full_name_field.send_keys("Бугаев Дмитрий")

        email_field = driver.find_element(By.ID, "userEmail")
        email_field.send_keys("bugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_dbugaev_d@example.com")

        current_address_field = driver.find_element(By.ID, "currentAddress")
        current_address_field.send_keys("Санкт-Петербург, Невский проспект, д.151")

        permanent_address_field = driver.find_element(By.ID, "permanentAddress")
        permanent_address_field.send_keys("Санкт-Петербург, Проспект Большевиков, д.32")

        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        time.sleep(2)

        result_box = driver.find_element(By.ID, "output")

        if len(result_box.text) > 0:
            print("Тест не пройден")
        else:
            print("Тест пройден")

    finally:
        driver.quit()