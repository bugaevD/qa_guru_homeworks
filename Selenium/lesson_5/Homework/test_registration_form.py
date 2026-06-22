import os
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from practice_form_page import PracticeForm, StudentForm


class TestRegistrationForm:

    def setup_method(self):
        self.registration_form = PracticeForm(webdriver.Chrome())
        self.registration_form.setup()
        self.tmp_file_name = self._create_tmp_file()

    def _create_tmp_file(self):
        file_path = os.path.abspath('test_file.jpg')
        with open(file_path, 'w') as file:
            file.write("Test")
        return file_path

    def teardown_method(self):
        if os.path.exists(self.tmp_file_name):
            os.remove(self.tmp_file_name)
        self.registration_form.tear_down()

    def test_positive(self):
        student = StudentForm(first_name="Dmitry", last_name="Bugaev", email="bugaev@example.com", gender="Male",
                              user_number="0123456789",
                              birth_date=("04", "3", "1996"), subjects=("Maths", "English"),
                              hobbies=("Sports", "Reading"),
                              current_address="г. Санкт-Петербург, ул. Невский проспект, д 101", state="NCR",
                              city="Noida", )
        self.registration_form.fill_form(student)
        result_form = self.registration_form.wait.until(
            ec.visibility_of_element_located(self.registration_form.RESULT_FORM)
        )
        print(result_form.text)
        self.registration_form.assert_positive_all_fields(student)

    def test_only_required_fields(self):
        student = StudentForm(first_name="Dmitry", last_name="Bugaev", email="bugaev@example.com", gender="Male",
                              user_number="0123456789", )
        self.registration_form.fill_form(student)
        self.registration_form.assert_required_fields(student)

    def test_empty_fields(self):
        self.registration_form.close_commercial_banner()
        self.registration_form.click_submit_button()
        self.registration_form.assert_form_error()

    def test_invalid_number(self):
        student = StudentForm(first_name="Dmitry", last_name="Bugaev", email="bugaev@example.com", gender="Male",
                              user_number="0129")
        self.registration_form.fill_form(student)
        self.registration_form.assert_form_error()
