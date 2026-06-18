import pytest
from selenium import webdriver

from text_box_form import TextBoxForm


class TestTextBoxForm:
    @pytest.fixture
    def driver(self):
        driver = webdriver.Chrome()
        yield driver
        driver.quit()

    @pytest.fixture
    def text_box_form(self, driver):
        text_box_form = TextBoxForm(driver)
        text_box_form.open_text_box_page()
        return text_box_form

    @pytest.mark.parametrize("full_name, email, current_address, permanent_address", [
        ("Bugaev Dmitry", "bugaev@example.com", "New-York, wall-street", "456 Oak St"),
        ("Бугаев Дмитрий", "bugaev@example.com", "Нью-Йорк, вал-стрит", "456 Дубовая ул"),
        ("A", "a@bk.ru", "B", "B"),
        ("Николай Римский-Корсаков", "bugaev_@example.com", "Невский 155/2", "Addr 3 & 4"),
        ("  Bugaev Dmitry  ", "  bugaev@example.com  ", "  New-York, wall-street  ", "  456 Oak St  "),
        ("Bugaev Dmitry", "BUGAEV@EXAMPLE.COM", "New-York, wall-street", "456 Oak St")
    ])
    def test_positive_data(self, text_box_form, full_name, email, current_address, permanent_address):
        text_box_form.fill_full_form(full_name, email, current_address, permanent_address)
        text_box_form.assert_valid_result(full_name, email, current_address, permanent_address)

    @pytest.mark.parametrize("full_name, email, current_address, permanent_address", [
        ("Bugaev Dmitry", "", "", ""),
        ("", "bugaev@example.com", "", ""),
        ("", "", "New-York, wall-street", ""),
        ("", "", "", "456 Oak St"),
        ("Bugaev Dmitry", "bugaev@example.com", "", "")
    ])
    def test_partial_form_submission(self, text_box_form, full_name, email, current_address, permanent_address):
        text_box_form.fill_full_form(full_name, email, current_address, permanent_address)
        text_box_form.assert_valid_result(full_name, email, current_address, permanent_address)

    # @pytest.mark.parametrize("email", [
    #     "bugaevexample.com",
    #     # "bugaev@examplecom", Форма пропускает данный email
    #     "@example.com",
    #     "bugaev@@example.com",
    #     "bugaev@example..com",
    #     "bugaev@.com",
    #     "bugaevexample"
    # ])
    # def test_invalid_email(self, text_box_form, email):
    #     text_box_form.fill_full_form(email=email)
    #     print(text_box_form.get_validation_message())
    #     text_box_form.assert_invalid_email(email=email)

    @pytest.mark.parametrize("email, error_message", [
        ("bugaevexample.com", '"Адрес электронной почты должен содержать символ "@". В адресе "bugaevexample.com" отсутствует символ "@".'),
        # "bugaev@examplecom", Форма пропускает данный email
        ("@example.com", 'Введите часть адреса до символа "@". Адрес "@example.com" неполный.'),
        ("bugaev@@example.com", 'Часть адреса после символа "@" не должна содержать символ "@".'),
        ("bugaev@example..com", 'Недопустимое положение символа "." в адресе "example..com".'),
        ("bugaev@.com", 'Недопустимое положение символа "." в адресе ".com".'),
        ("bugaevexample", 'Адрес электронной почты должен содержать символ "@". В адресе "bugaevexample" отсутствует символ "@".')
    ])
    def test_invalid_email(self, text_box_form, email, error_message):
        text_box_form.fill_full_form(email=email)
        print(text_box_form.get_validation_message())
        text_box_form.assert_invalid_email(email=email, error_message=error_message)

    @pytest.mark.parametrize("full_name, email, current_address, permanent_address", [
        (f"{"Bugaev Dmitry" * 100}", "bugaev@example.com", "New-York, wall-street", "456 Oak St"),
        ("Bugaev Dmitry", f"{"bugaev" * 11}@example.com", "New-York, wall-street", "456 Oak St"),
        ("Bugaev Dmitry", "bugaev@example.com", f"{"New-York, wall-street" * 100}", "456 Oak St"),
        ("Bugaev Dmitry", "bugaev@example.com", "New-York, wall-street", f"{"456 Oak St" * 100}")
    ])
    @pytest.mark.xfail
    def test_long_data(self, text_box_form, full_name, email, current_address, permanent_address):
        text_box_form.fill_full_form(full_name, email, current_address, permanent_address)
        text_box_form.assert_long_data()

    @pytest.mark.parametrize("full_name, email, current_address, permanent_address", [
        ("", "", "", "")
    ])
    @pytest.mark.xfail
    def test_empty_fields(self, text_box_form, full_name, email, current_address, permanent_address):
        text_box_form.fill_full_form(full_name, email, current_address, permanent_address)
        text_box_form.assert_empty_fields()

    @pytest.mark.parametrize("security_payload", [
        "<script>alert('xss')</script>",
        "1' OR '1'='1",
        ":):):):))))::;)",
        "<div>HTML injection</div>"
    ])
    def test_security_payload(self, text_box_form, security_payload):
        text_box_form.fill_full_form(full_name=security_payload)
        text_box_form.assert_security_payload(security_payload)
