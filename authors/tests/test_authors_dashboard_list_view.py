from django.test import TestCase
from django.urls import resolve, reverse

from authors import views

from .test_authors_mixin import AuthorsMixin


class AuthorsViewDashboardTestCase(TestCase, AuthorsMixin):

    def test_dashboard_view_is_correct(self):
        url = reverse('authors:dashboard')
        view = resolve(url)

        self.assertEqual(view.func.view_class, views.DashboardRecipeListView)

    def test_dashboard_user_is_not_authenticated(self):
        # usuario nao autenticado nao pode entra na dashboard

        # rotar para fazer o login
        login_url = reverse('authors:login')

        url = reverse('authors:dashboard')
        response = self.client.get(url)

        self.assertRedirects(response, login_url + '?next=' + url)

    def test_dashboard_view_loads_correct_template(self):
        self.make_login_author()
        url = reverse('authors:dashboard')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'authors/views/dashboard.html')

    def test_dashboard_title_is_correct(self):
        user = self.make_login_author()
        url = reverse('authors:dashboard')
        response = self.client.get(url)
        title = f'Dashboard ({user.username})'
        self.assertIn(title, response.content.decode('utf-8'))

    def test_dashboard_list_recipes_is_correct(self):
        user = self.make_login_author()
        recipe = self.make_recipe(user=user)

        recipes = []
        recipes.append(recipe)

        for i in range(4):
            new_recipe = self.make_recipe(
                user=user,
                title=f'{recipe.title}-{i}'
            )
            recipes.append(new_recipe)

        url = reverse('authors:dashboard')
        response = self.client.get(url)
        for item in recipes:
            self.assertIn(item.title, response.content.decode('utf-8'))

    def test_dashboard_list_recipe_is_published(self):
        user = self.make_login_author()
        recipe = self.make_recipe(user=user)
        recipe.is_published = True
        recipe.save()

        url = reverse('authors:dashboard')
        response = self.client.get(url)

        self.assertNotIn(recipe.title, response.content.decode('utf-8'))
