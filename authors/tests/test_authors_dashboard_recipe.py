from django.test import TestCase
from django.urls import resolve, reverse

from authors import views

from .test_authors_mixin import AuthorsMixin


class AuthorsViewDashboardRecipeNewTestCase(TestCase, AuthorsMixin):

    def test_dashboard_recipe_new_is_correct(self):
        url = reverse('authors:dashboard_recipe_new')
        view = resolve(url)

        self.assertEqual(view.func.view_class, views.DashboardRecipe)

    def test_dashboard_recipe_edit_is_correct(self):
        url = reverse('authors:dashboard_recipe_edit', kwargs={'id': 1})
        view = resolve(url)

        self.assertEqual(view.func.view_class, views.DashboardRecipe)

    def test_dashboard_recipe_new_user_is_not_authenticated(self):
        # usuario nao autenticado nao pode entra na dashboard

        # rotar para fazer o login
        login_url = reverse('authors:login')

        url = reverse('authors:dashboard_recipe_new')
        response = self.client.get(url)

        self.assertRedirects(response, login_url + '?next=' + url)

    def test_dashboard_recipe_new_view_loads_correct_template(self):
        self.make_login_author()
        url = reverse('authors:dashboard_recipe_new')
        response = self.client.get(url)
        self.assertTemplateUsed(
            response, 'authors/views/dashboard_recipe_form.html')


class AuthorsViewDashboardRecipeEditTestCase(TestCase, AuthorsMixin):

    def test_dashboard_recipe_edit_is_correct(self):
        url = reverse('authors:dashboard_recipe_edit', kwargs={'id': 1})
        view = resolve(url)

        self.assertEqual(view.func.view_class, views.DashboardRecipe)

    def test_dashboard_recipe_id_user_is_not_authenticated(self):
        # usuario nao autenticado nao pode entra na dashboard

        # rotar para fazer o login
        login_url = reverse('authors:login')

        url = reverse('authors:dashboard_recipe_edit', kwargs={'id': 1})
        response = self.client.get(url)

        self.assertRedirects(response, login_url + '?next=' + url)

    def test_dashboard_recipe_edit_view_loads_correct_template(self):
        user = self.make_login_author()
        self.make_recipe(user=user)
        url = reverse('authors:dashboard_recipe_edit', kwargs={'id': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(
            response, 'authors/views/dashboard_recipe_form.html')

    def test_dashboard_recipe_edit_id_not_match_not_found(self):
        user = self.make_login_author()
        self.make_recipe(user=user)
        url = reverse('authors:dashboard_recipe_edit', kwargs={'id': 2})
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)


class AuthorsDashboardRecipeDeleteTestCase(TestCase, AuthorsMixin):

    def test_dashboard_recipe_delete_user_is_not_authenticated(self):
        # usuario nao autenticado nao pode entra na dashboard

        # rotar para fazer o login
        login_url = reverse('authors:login')

        url = reverse('authors:dashboard_recipe_delete')
        response = self.client.post(url, data={'id': 1}, follow=True)

        self.assertRedirects(response, login_url + '?next=' + url)

    def test_dashboard_recipe_delete_method_get(self):
        self.make_login_author()
        url = reverse('authors:dashboard_recipe_delete')
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_dashboard_recipe_delete_successfully(self):
        user = self.make_login_author()
        recipe = self.make_recipe(user=user)
        url = reverse('authors:dashboard_recipe_delete')

        response = self.client.post(url, data={'id': recipe.id}, follow=True)
        msg = 'Recipe successfully deleted.'
        self.assertIn(msg, response.content.decode('utf-8'))
