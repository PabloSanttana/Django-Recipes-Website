from django.test import TestCase
from django.urls import reverse


class AuthorsUrlsTestCase(TestCase):
    def test_authors_Register_is_correct(self):
        url = reverse('authors:register')
        self.assertEqual(url, '/authors/register/')

    def test_authors_create_is_corretc(self):
        url = reverse('authors:create')
        self.assertEqual(url, '/authors/register/create')
