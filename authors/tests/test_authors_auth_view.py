from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from authors import views


class AuthorsViewAuthTestCase(TestCase):
    def make_create_author(self):
        # cria um usuario
        self.user_password = 'Ab123456789'
        user = User.objects.create_user(
            username='RafaelaDarc',
            last_name='Darc',
            first_name='Rafaela',
            email='RafaelaDarc@gmail.com',
            password=self.user_password)
        return user

    def make_login_author(self):
        user = self.make_create_author()
        self.client.login(username=user.username, password=self.user_password)
        return user

    def test_authors_login_view_is_correct(self):
        url = reverse('authors:login')
        view = resolve(url)

        self.assertIs(view.func, views.login_view)

    def test_authors_login_view_loads_correct_template(self):
        url = reverse('authors:login')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'authors/views/login.html')

    def test_authors_login_create_method_get_return_404(self):
        url = reverse('authors:login_create')
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)

    def test_authors_login_create_form_invalid(self):
        url = reverse('authors:login_create')
        response = self.client.post(url,  data={
            'username': '',
            'password': '',
        }, follow=True)
        msg = 'Invalid username or password.'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_authors_login_create_invalid_credentials(self):
        url = reverse('authors:login_create')
        response = self.client.post(url,  data={
            'username': 'guilherme',
            'password': 'Abcd123456',
        }, follow=True)
        msg = 'Invalid credentials'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_authors_login_create_success(self):

        user = self.make_create_author()
        # login do usuario
        url = reverse('authors:login_create')

        response = self.client.post(url,  data={
            'username': user.username,
            'password': self.user_password,
        }, follow=True)

        msg = 'Your are logged in.'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_authors_logout_view_unauthenticated_user(self):
        # rotar para fazer o logout
        logout_url = reverse('authors:logout')
        # rotar para fazer o login
        login_url = reverse('authors:login')

        response = self.client.get(logout_url)
        # usuario precisa esta logador para acessar essa page
        # logo iria ser redirecionado para login, depois de logado volta
        # para pagina que desejou acessar anteriormente
        self.assertRedirects(response, login_url + '?next=' + logout_url)

    def test_authors_logout_view_redirects_if_not_post(self):
        self.make_login_author()

        logout_url = reverse('authors:logout')
        login_url = reverse('authors:login')

        response = self.client.get(logout_url)
        # code de redirect 302
        self.assertEqual(302, response.status_code)

        # Check that the redirect goes to the login page
        self.assertEqual(response.url, login_url)

    def test_authors_logout_view_redirects_if_username_does_not_match(self):
        self.make_login_author()

        logout_url = reverse('authors:logout')

        response = self.client.post(
            logout_url, data={'username': 'rafael'}, follow=True)

        msg = 'Your are logged in with RafaelaDarc.'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_authors_logout_view_sucess(self):
        user = self.make_login_author()

        logout_url = reverse('authors:logout')

        response = self.client.post(
            logout_url, data={'username': user.username}, follow=True)

        msg = 'Your are logged in with RafaelaDarc.'
        self.assertNotIn(msg, response.content.decode('utf-8'))
