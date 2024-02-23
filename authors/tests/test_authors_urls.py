from django.test import TestCase
from django.urls import reverse


class AuthorsUrlsTestCase(TestCase):
    def test_authors_Register_is_correct(self):
        url = reverse('authors:register')
        self.assertEqual(url, '/authors/register/')

    def test_authors_create_is_corretc(self):
        url = reverse('authors:create')
        self.assertEqual(url, '/authors/register/create/')

    def test_authors_login_is_corretc(self):
        url = reverse('authors:login')
        self.assertEqual(url, '/authors/login/')

    def test_authors_login_create_is_corretc(self):
        url = reverse('authors:login_create')
        self.assertEqual(url, '/authors/login/create/')

    def test_authors_logout_is_corretc(self):
        url = reverse('authors:logout')
        self.assertEqual(url, '/authors/logout/')

    def test_authors_dashboard_is_correct(self):
        url = reverse('authors:dashboard')
        self.assertEqual(url, '/authors/dashboard/')
