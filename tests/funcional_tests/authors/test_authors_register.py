
import pytest
from parameterized import parameterized
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseFunctionalTest


@pytest.mark.functional_test
class AuthorsRegisterFunctionalTest(AuthorsBaseFunctionalTest):

    def fill_form_data(self, form):
        for key, value in self.form_data.items():
            field = form.find_element(By.NAME, key)
            field.send_keys(value)

    def get_form(self):
        form = self.browser.find_element(
            By.ID, 'register_user')

        return form

    @parameterized.expand([
        ('username', 'This field must not be empty.'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('email', 'The e-mail must be valid.'),
        ('password', 'Password must not be empty')
    ])
    def test_missing_or_invalid_input_error_message(self, name_field,
                                                    error_message):
        """
        Test error messages for missing or invalid input in each form field.
        """
        # User opens the browser on the registration form
        self.browser.get(self.live_server_url + '/authors/register/')

        # Select the form
        form = self.get_form()

        # Fill the form fields with data
        self.fill_form_data(form)

        # However, forgets to fill a field or
        # mistakenly enters an invalid email

        field = form.find_element(By.NAME, name_field)
        field.clear()
        if name_field == 'email':
            field.send_keys('email@com')
        else:
            field.send_keys(' ' * 20)

        # Submit the form
        form.submit()

        form = self.get_form()

        # Check the error message for the field that was not filled correctly
        self.assertIn(error_message, form.text)

    def test_authors_register_sucess(self):
        # Usuario abre o navegador
        self.browser.get(self.live_server_url + '/authors/register/')

        # usuario seleciona o formulario
        form = self.get_form()

        # preenche o formulario com dados validos
        self.fill_form_data(form)

        # faz o envio do formulario
        form.submit()

        msg = 'Your user is created successfully, please log in.'

        # ver a messagen na tela de usuario criado com sucesso.
        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn(msg, body.text)
