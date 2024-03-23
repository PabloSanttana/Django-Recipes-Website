from django.test import TestCase, override_settings
from django.urls import resolve, reverse

from authors import views

from .test_authors_mixin import AuthorsMixin


class AuthorsViewAuthenticationTestCase(TestCase, AuthorsMixin):

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

    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_authors_logout_view_redirects_if_username_does_not_match(self):

        self.make_login_author()

        logout_url = reverse('authors:logout')

        response = self.client.post(
            logout_url, data={'username': 'rafael'}, follow=True)

        msg = 'Your are logged in with RafaelaDarc.'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_authors_logout_view_sucess(self):
        # Faz login como um autor e obtém o usuário logado
        user = self.make_login_author()

        # Obtém a URL reversa para a visualização de logout
        logout_url = reverse('authors:logout')

        # Realiza uma solicitação POST para a URL de logout com os dados
        # de usuário
        response = self.client.post(
            logout_url, data={'username': user.username}, follow=True)

        # Define uma mensagem que é exibida quando um usuário está logado
        msg = 'You are logged in with RafaelaDarc.'

        # Verifica se a mensagem não está presente no conteúdo da resposta
        # Isso garante que o logout tenha sido bem-sucedido e o
        # usuário não esteja mais logado
        self.assertNotIn(msg, response.content.decode('utf-8'))
