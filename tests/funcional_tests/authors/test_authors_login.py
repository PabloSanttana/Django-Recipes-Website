
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .test_base import AuthorsBaseFunctionalTest

# from selenium.webdriver.common.keys import Keys


@pytest.mark.functional_test
class AuthorsLoginFunctionalTest(AuthorsBaseFunctionalTest):

    def make_create_user(self):
        User.objects.create_user(
            username='rafaelaDarc', password='Abc123456')

    def test_authors_login_valid_data_succes(self):
        self.make_create_user()
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.ID, 'login_user')

        form.find_element(By.NAME, 'username').send_keys('rafaelaDarc')
        form.find_element(By.NAME, 'password').send_keys('Abc123456')
        form.submit()
        msg = 'Your are logged in.'

        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn(msg, body.text)

    def test_authors_login_invalid_credentials(self):

        self.make_create_user()
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.ID, 'login_user')

        form.find_element(By.NAME, 'username').send_keys('rafaelaDarck')
        form.find_element(By.NAME, 'password').send_keys('Abc1234561')
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
