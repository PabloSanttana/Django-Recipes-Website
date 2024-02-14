
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .test_base import AuthorsBaseFunctionalTest

# from selenium.webdriver.common.keys import Keys


@pytest.mark.functional_test
class AuthorsLoginFunctionalTest(AuthorsBaseFunctionalTest):

    def make_create_author(self):
        # cria um usuario
        password = 'Ab123456789'
        user = User.objects.create_user(
            username='RafaelaDarc',
            last_name='Darc',
            first_name='Rafaela',
            email='RafaelaDarc@gmail.com',
            password=password)
        return (user.username, password)

    def test_authors_login_invalid_credentials(self):

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.ID, 'login_user')

        form.find_element(By.NAME, 'username').send_keys('RafaelaDarc')
        form.find_element(By.NAME, 'password').send_keys('Ab123456789')
        form.submit()
        msg = 'Invalid credentials'

        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn(msg, body.text)

    def test_authors_login_invalid_data(self):

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.ID, 'login_user')

        form.find_element(By.NAME, 'username').send_keys('    ')
        form.find_element(By.NAME, 'password').send_keys('     ')
        form.submit()
        msg = 'Invalid username or password.'

        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn(msg, body.text)

    def test_authors_login_valid_data_succes(self):
        # Obtém as credenciais de um usuário criado anteriormente
        username, password = self.make_create_author()

        # Navega até a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Localiza o formulário de login na página
        form = self.browser.find_element(By.ID, 'login_user')

        # Preenche o nome de usuário e a senha nos campos
        # de entrada do formulário
        form.find_element(By.NAME, 'username').send_keys(username)
        form.find_element(By.NAME, 'password').send_keys(password)

        # Submete o formulário para fazer login
        form.submit()

        # Verifica se a mensagem 'Your are logged in.'
        # está presente no corpo da página
        # Isso indica que o usuário foi deslogado com sucesso
        msg = 'Your are logged in.'

        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn(msg, body.text)

    def test_authors_logout_success(self):
        # Obtém as credenciais de um usuário criado anteriormente
        username, password = self.make_create_author()

        # Navega até a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Localiza o formulário de login na página
        form = self.browser.find_element(By.ID, 'login_user')

        # Preenche o nome de usuário e a senha
        # nos campos de entrada do formulário
        form.find_element(By.NAME, 'username').send_keys(username)
        form.find_element(By.NAME, 'password').send_keys(password)

        # Submete o formulário para fazer login
        form.submit()

        # Localiza e submete o formulário de logout
        form = self.browser.find_element(By.ID, 'form_logout')
        form.submit()

        # Verifica se a mensagem 'Your are logged in.'
        # não está presente no corpo da página
        # Isso indica que o usuário foi deslogado com sucesso
        msg = 'Your are logged in.'
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertNotIn(msg, body.text)
