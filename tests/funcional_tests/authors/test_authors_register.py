
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseFunctionalTest


@pytest.mark.functional_test
class AuthorsRegisterFunctionalTest(AuthorsBaseFunctionalTest):

    def fill_form_dummy_data(self, form):

        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def fill_form_data(self, form):
        for key, value in self.form_data.items():
            field = form.find_element(By.NAME, key)
            field.send_keys(value)

    def test_empty_first_name_error_message(self):

        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.browser.find_element(
            By.ID, 'register_user')

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        form.find_element(By.NAME, 'first_name').send_keys(Keys.ENTER)

        form = self.browser.find_element(
            By.ID, 'register_user')

        self.assertIn('Write your first name', form.text)

    def test_authors_register_sucess(self):
        self.browser.get(self.live_server_url + '/authors/register/')

        form = self.browser.find_element(
            By.ID, 'register_user')

        self.fill_form_data(form)

        form.find_element(By.NAME, 'first_name').send_keys(Keys.ENTER)

        msg = 'Your user is created successfully, please log in.'

        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn(msg, body.text)
