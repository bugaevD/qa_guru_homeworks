import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PracticeForm:
    PRACTICE_FROM_TITLE = (By.XPATH, "//main//h1")
    FIRST_NAME_FIELD = (By.ID, "firstName")
    LAST_NAME_FIELD = (By.ID, "lastName")
    EMAIL_FIELD = (By.ID, "userEmail")
    USER_NUMBER_FIELD = (By.ID, "userNumber")
    CALENDAR_INPUT = (By.ID, "dateOfBirthInput")
    YEAR_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__year-select")
    MONTH_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__month-select")
    DAY_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__day--025:not(.react-datepicker__day--outside-month)")
    SUBJECT_FIELD = (By.ID, "subjectsInput")
    SPORTS_HOBBY_CHECK_BOX = (By.XPATH, "//input[@value='Sports']")
    READING_HOBBY_CHECK_BOX = (By.XPATH, "//input[@value='Reading']")
    UPLOAD_PICTURE_BUTTON = (By.ID, "uploadPicture")
    CURRENT_ADDRESS_FIELD = (By.ID, "currentAddress")
    STATE_INPUT = (By.ID, "state")
    STATE_SELECT = (By.XPATH, "//div[@id='stateCity-wrapper']/div[contains(text(), 'NCR')]")
    CITY_INPUT = (By.ID, "city")
    CITY_SELECT = (By.XPATH, "//div[@id='stateCity-wrapper']/div[contains(text(), 'Noida')]")
    SUBMIT_BUTTON = (By.ID, "submit")
    BANNER_BUTTON = (By.XPATH, "//div[@id='fixedban']//button[@aria-label='Close']")
    RESULT_FORM = (By.ID, "resultModal")

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"
        self.wait = WebDriverWait(self.driver, 10)

    def tear_up(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    def tear_down(self):
        if os.path.exists('test.jpg'):
            os.remove('test.jpg')
        self.driver.quit()

    def close_commercial_banner(self):
        self.wait.until(EC.element_to_be_clickable(self.BANNER_BUTTON)).click()

    def fill_first_name(self, first_name):
        self.driver.find_element(*self.FIRST_NAME_FIELD).send_keys(first_name)

    def fill_last_name(self, last_name):
        self.driver.find_element(*self.LAST_NAME_FIELD).send_keys(last_name)

    def fill_email(self, user_email):
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(user_email)

    def select_gender(self, gender):
        gender_radio_button = self.driver.find_element(By.XPATH, f"//input[@value='{gender}']")
        gender_radio_button.click()

    def fill_user_number(self, user_number):
        self.driver.find_element(*self.USER_NUMBER_FIELD).send_keys(user_number)

    def select_date_of_birth(self, year, month):
        self.driver.find_element(*self.CALENDAR_INPUT).click()
        Select(self.driver.find_element(*self.YEAR_OF_BIRTH_SELECT)).select_by_value(year)
        Select(self.driver.find_element(*self.MONTH_OF_BIRTH_SELECT)).select_by_value(month)
        self.driver.find_element(*self.DAY_OF_BIRTH_SELECT).click()

    def fill_subject(self, *subjects):
        subjects_input = self.driver.find_element(*self.SUBJECT_FIELD)
        for subject in subjects:
            subjects_input.send_keys(subject)
            subjects_input.send_keys(Keys.ENTER)

    def select_hobbies(self):
        self.driver.find_element(*self.SPORTS_HOBBY_CHECK_BOX).click()
        self.driver.find_element(*self.READING_HOBBY_CHECK_BOX).click()

    def upload_image(self):
        with open("test.jpg", "w") as file:
            file.write("Test")
        file_path = os.path.abspath("test.jpg")
        self.driver.find_element(*self.UPLOAD_PICTURE_BUTTON).send_keys(file_path)

    def fill_current_address(self, current_address):
        self.driver.find_element(*self.CURRENT_ADDRESS_FIELD).send_keys(current_address)

    def select_state(self):
        self.driver.find_element(*self.STATE_INPUT).click()
        self.wait.until(EC.element_to_be_clickable(self.STATE_SELECT)).click()

    def select_city(self):
        self.driver.find_element(*self.CITY_INPUT).click()
        self.wait.until(EC.element_to_be_clickable(self.CITY_SELECT)).click()

    def submit_form(self):
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def final_result(self):
        self.driver.find_element(*self.RESULT_FORM).click()

practice_form = PracticeForm()

practice_form.tear_up()
practice_form.close_commercial_banner()
practice_form.fill_first_name("Dmitry")
practice_form.fill_last_name("Bugaev")
practice_form.fill_email("bugaev@example.com")
practice_form.select_gender("Female")
practice_form.fill_user_number("1234567890")
practice_form.select_date_of_birth("1988", "4")
practice_form.fill_subject("Maths", "English")
practice_form.select_hobbies()
practice_form.upload_image()
practice_form.fill_current_address("г. Санкт-Петербург, ул. Невский проспект, д 101")
practice_form.select_state()
practice_form.select_city()
practice_form.submit_form()
practice_form.tear_down()