from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()

try:
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")

    driver.find_element(By.ID, "username").send_keys("Иван Иванов")
    driver.find_element(By.ID, "userEmail").send_keys("ivan@example.com")
    driver.find_element(By.ID, "currentAddress").send_keys("ул. Ленина, дом 1")
    driver.find_element(By.ID, "permanentAddress    ").send_keys("ул. Пушкина, дом 10")

    submit_button = driver.find_element(By.ID, "submit")
    driver.execute_script("arguments[0].scrollIntoView();", submit_button)

    fluent_wait = WebDriverWait(
        driver,
        timeout=10,
        poll_frequency=0.5,
        ignored_exceptions=[NoSuchElementException, StaleElementReferenceException]
    )

    output_block = fluent_wait.until(EC.presence_of_element_located((By.ID, "output")))

    print("Тест успешно пройден! Блок с результатами появился.")
    assert output_block.is_displayed()

finally:
    driver.quit()