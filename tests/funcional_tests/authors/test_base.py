
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from utils.browser import make_chrome_browser


class AuthorsBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        self.form_data = {
            'username': 'RafaelaDarc',
            'first_name': 'Rafaela',
            'last_name': 'Darc',
            'email': 'RafaelaDarc@gmail.com',
            'password': 'Ab123456789',
            'password2': 'Ab123456789',
        }
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, s=5):
        time.sleep(s)
