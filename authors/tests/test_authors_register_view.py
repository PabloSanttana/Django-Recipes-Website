from django.test import TestCase
from django.urls import resolve, reverse

from authors import views


class AuthorsViewRegisterTestCase(TestCase):

    def test_authors_register_view_is_correct(self):
        url = reverse('authors:register')
        view = resolve(url)

        self.assertIs(view.func, views.register_view)

    def test_authors_register_view_loads_correct_template(self):
        url = reverse('authors:register')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'authors/views/register.html')
