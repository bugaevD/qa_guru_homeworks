import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class CalendarElement:
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator

    @property
    def element(self):
        return self.driver.find_element(*self.locator)

    def get_headers(self):
        header_elements = self.driver.find_elements(By.CSS_SELECTOR, "thead th")
        return [header.text for header in header_elements]

    def get_row_data(self, row_index):
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        cells = rows[row_index].find_elements(By.TAG_NAME, "td")
        return [cell.text for cell in cells]

    def get_cell_value(self, row_index, column_index):
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        cells = rows[row_index].find_elements(By.TAG_NAME, "td")
        return cells[column_index].text


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)

    try:
        driver.get("https://the-internet.herokupp.com/tables")

        table1_locator = (By.ID, "table1")
        table = (driver, table1_locator)

        headers = table.get_headers()
        first_row = table.get_row_data(0)
        specific_cell = table.get_cell_value(row_index=2, column_index=3)  # Строка 3, Колонка 4

        print("Заголовки таблицы:", headers)
        print("Первая строка данных:", first_row)
        print(f"Значения в строке колонке 'Due': {specific_cell}")

        assert "Last Name" in headers, "Заголовок 'Last Name', не найден"
        assert "Smith" in first_row, "Фамилия 'Smith' должна быть в первой строке"
        assert specific_cell == "$100.00", f""
    finally:
        pass
