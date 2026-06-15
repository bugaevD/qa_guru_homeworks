import os

from selenium import webdriver
from selenium_lesson_5_homework_registration_form_v3_test import PracticeForm


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
        self.registration_form.fill_form("Dmitry", "Bugaev", "bugaev@example.com", "Male", "0123456789",
                                         ("04", "3", "1996"), ("Maths", "English"),
                                         ("Sports", "Reading"),
                                                     "г. Санкт-Петербург, ул. Невский проспект, д 101", "NCR", "Noida")
        self.registration_form.assert_positive_all_fields("Dmitry", "Bugaev", "bugaev@example.com", "Male",
                                                          "0123456789", ("04", "3", "1996"), ("Maths", "English"),
                                                          ("Sports", "Reading"),
                                                          "г. Санкт-Петербург, ул. Невский проспект, д 101", "NCR",
                                                          "Noida", "test_file.jpg")

    def test_only_required_fields(self):
        self.registration_form.fill_form("Dmitry", "Bugaev", "bugaev@example.com", "Male", "0123456789")
        self.registration_form.assert_required_fields("Dmitry", "Bugaev", "bugaev@example.com", "Male", "0123456789")

    def test_empty_fields(self):
        self.registration_form.close_commercial_banner()
        self.registration_form.click_submit_button()
        self.registration_form.assert_empty_fields()

    def test_invalid_number(self):
        self.registration_form.fill_form("Dmitry", "Bugaev", "bugaev@example.com", "Male", "0129")
        self.registration_form.assert_invalid_number()
