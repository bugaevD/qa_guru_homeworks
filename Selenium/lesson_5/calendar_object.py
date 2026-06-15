from typing import Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Calendar:
    SELECT_YEAR = (By.CSS_SELECTOR, ".react-datepicker__year-select")
    SELECT_MONTH = (By.CSS_SELECTOR, ".react-datepicker__month-select")

    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator
        self.wait = WebDriverWait(self.driver, 5)

    @property
    def element(self):
        return self.driver.find_element(*self.locator)

    def select_calendar(self):
        self.element.click()
        self.wait.until(ec.visibility_of_element_located(self.SELECT_YEAR))

    def select_birth_day(self, date: Tuple[str, str, str]):
        """
        Заполнить поле с датой
        :param date: день(01-31), месяц(название месяца по-английски(April)), год(например 1996)
        :return:
        """
        Select(self.driver.find_element(*self.SELECT_YEAR)).select_by_value(date[2])
        Select(self.driver.find_element(*self.SELECT_MONTH)).select_by_visible_text(date[1])
        self.driver.find_element(By.CSS_SELECTOR, f".react-datepicker__day--0{date[0]}[tabindex='0']").click()
