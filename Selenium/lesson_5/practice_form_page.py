import os
import time
from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from calendar_object import Calendar


class PracticeForm:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)
        self.url = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"
        self.calendar = Calendar(driver, (By.ID, "dateOfBirthInput"))

    PRACTICE_FORM_TITLE = (By.XPATH, "//main//h1")
    FIRST_NAME_FIELD = (By.ID, "firstName")
    LAST_NAME_FIELD = (By.ID, "lastName")
    EMAIL_FIELD = (By.ID, "userEmail")
    USER_NUMBER_FIELD = (By.ID, "userNumber")
    CALENDAR_INPUT = (By.ID, "dateOfBirthInput")
    YEAR_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__year-select")
    MONTH_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__month-select")
    SUBJECT_FIELD = (By.ID, "subjectsInput")
    UPLOAD_PICTURE_BUTTON = (By.ID, "uploadPicture")
    CURRENT_ADDRESS_FIELD = (By.ID, "currentAddress")
    STATE_INPUT = (By.ID, "state")
    CITY_INPUT = (By.ID, "city")
    SUBMIT_BUTTON = (By.ID, "submit")
    BANNER_BUTTON = (By.XPATH, "//div[@id='fixedban']//button[@aria-label='Close']")
    RESULT_FORM = (By.ID, "resultModal")
    FORM_ERROR = (By.ID, "formError")

    def setup(self):
        self.driver.set_window_size(1280, 720)
        self.driver.get(self.url)
        self.test_file = self.create_test_file()

    def close_commercial_banner(self):
        banner_button = self.wait.until(ec.element_to_be_clickable(self.BANNER_BUTTON))
        banner_button.click()

    def get_form_error(self):
        return self.driver.find_element(*self.FORM_ERROR).text

    def fill_first_name(self, first_name):
        if first_name is None:
            return
        firstname_field = self.driver.find_element(*self.FIRST_NAME_FIELD)
        firstname_field.send_keys(first_name)

    def fill_last_name(self, last_name):
        if last_name is None:
            return
        lastname_field = self.driver.find_element(*self.LAST_NAME_FIELD)
        lastname_field.send_keys(last_name)

    def fill_email(self, email):
        if email is None:
            return
        email_field = self.driver.find_element(*self.EMAIL_FIELD)
        email_field.send_keys(email)

    def fill_user_number(self, user_number):
        if user_number is None:
            return
        user_number_field = self.driver.find_element(*self.USER_NUMBER_FIELD)
        user_number_field.send_keys(user_number)

    def select_gender(self, gender):
        if gender is None:
            return
        gender_radio_button = self.driver.find_element(By.XPATH,
                                                    f"//div[@id='genterWrapper']//input[@value='{gender}']")
        gender_radio_button.click()

    def select_birth_day(self, date: Tuple[str, str, str]):
        if date is None:
            return
        self.calendar.select_calendar()
        self.calendar.select_birth_day(date)

    def create_test_file(self):
        file_path = os.path.abspath('test_file.jpg')
        with open(file_path, 'w') as file:
            file.write("Test")
        return file_path

    def upload_file(self, file_path):
        self.driver.find_element(*self.UPLOAD_PICTURE_BUTTON).send_keys(file_path)

    def fill_subject(self, subjects):
        if subjects is None:
            return
        subjects_input = self.driver.find_element(*self.SUBJECT_FIELD)
        self.driver.execute_script("arguments[0].scrollIntoView();", subjects_input)
        for subject in subjects:
            subjects_input.send_keys(subject)
            subjects_input.send_keys(Keys.ENTER)

    def select_hobbies(self, hobbies):
        if hobbies is None:
            return
        for hobby in hobbies:
             hobby_check_box = self.driver.find_element(By.XPATH,
                                                       f"//div[@id='hobbiesWrapper']//input[@value='{hobby}']")
             hobby_check_box.click()

    def fill_current_address(self, current_address):
        if current_address is None:
            return
        current_address_field = self.driver.find_element(*self.CURRENT_ADDRESS_FIELD)
        current_address_field.send_keys(current_address)

    def select_state(self, state):
        if state is None:
            return
        self.driver.find_element(*self.STATE_INPUT).click()
        state_dropdown = self.wait.until(
             ec.element_to_be_clickable((By.XPATH, f"//div[@class='state-city-option'][text()='{state}']")))
        state_dropdown.click()

    def select_city(self, city):
        if city is None:
            return
        self.driver.find_element(*self.CITY_INPUT).click()
        city_dropdown = self.wait.until(
            ec.element_to_be_clickable((By.XPATH, f"//div[@class='state-city-option'][text()='{city}']")))
        city_dropdown.click()

    def click_submit_button(self):
        submit_button = self.driver.find_element(*self.SUBMIT_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        submit_button.click()

    def fill_form(self, first_name=None, last_name=None, email=None, gender=None, user_number=None,
                  birth_date=None, subjects=None, hobbies=None, current_address=None, state=None,
                  city=None):

        practice_form_title = self.driver.find_element(*self.PRACTICE_FORM_TITLE)
        assert practice_form_title.text == "Practice Form", "Заголовок страницы не совпадает"

        self.close_commercial_banner()
        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_email(email)
        self.select_gender(gender)
        self.fill_user_number(user_number)
        self.select_birth_day(birth_date)
        self.fill_subject(subjects)
        self.select_hobbies(hobbies)
        self.upload_file(self.test_file)
        self.fill_current_address(current_address)
        self.select_state(state)
        self.select_city(city)
        self.click_submit_button()

    def assert_positive_all_fields(self, first_name=None, last_name=None, email=None, gender=None, user_number=None,
                                   birth_date=None, subjects=None, hobbies=None, current_address=None, state=None,
                                   city=None, file_name=None, ):
        result_form = self.wait.until(ec.visibility_of_element_located(self.RESULT_FORM))
        assert result_form.is_displayed(), "Таблица с данным не отобразилась"

        subjects = ", ".join(subjects) if isinstance(subjects, tuple) else subjects
        hobbies = ", ".join(hobbies) if isinstance(hobbies, tuple) else hobbies
        if isinstance(birth_date, tuple):
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            month_name = months[int(birth_date[1])]
            birth_date = f"{birth_date[0]} {month_name} {birth_date[2]}"
        else:
            birth_date = birth_date

        result_text = result_form.text
        expected_data = {
            "Student Name": f"{first_name} {last_name}",
            "Student Email": email,
            "Gender": gender,
            "Mobile": user_number,
            "Date of Birth": birth_date,
            "Subjects": subjects,
            "Hobbies": hobbies,
            "Picture": file_name,
            "Address": current_address,
            "State and City": f"{state} {city}"
        }

        for key, value in expected_data.items():
            assert key in result_text and value in result_text, f"Значения {value} из строки {key} не совпадают!"

    def assert_required_fields(self, first_name, last_name, email, gender, user_number):
        result_form = self.wait.until(ec.visibility_of_element_located(self.RESULT_FORM))
        assert result_form.is_displayed(), "Таблица с данным не отобразилась"

        result_text = result_form.text
        assert f"{first_name} {last_name}" in result_text, "Имя не найдено"
        assert email in result_text, "Email не найден"
        assert gender in result_text, "Пол не совпадает"
        assert user_number in result_text, "Номер телефона не найден"

    def assert_form_error(self):
        self.wait.until(ec.visibility_of_element_located(self.FORM_ERROR))
        error_message = self.get_form_error()
        assert error_message == "Please fill required fields and enter a valid 10-digit mobile number."

    def tear_down(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.driver.quit()
