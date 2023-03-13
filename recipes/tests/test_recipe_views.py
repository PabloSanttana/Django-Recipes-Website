
from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase

# Create your tests here.


class RecipeViewsTest(RecipeTestBase):

    # home
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:home')
        )
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(
            reverse('recipes:home')
        )
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(
            reverse('recipes:home')
        )
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(
            reverse('recipes:home')
        )
        self.assertIn('Não temos Receitas Publicadas ainda.',
                      response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        # create recipes for test
        self.make_recipe()
        response = self.client.get(
            reverse('recipes:home')
        )
        content = response.content.decode('utf-8')
        context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertIn('30 Minutos', content)
        self.assertIn('Recipe description', content)
        self.assertIn('Pablo', content)
        self.assertIn('category', content)
        self.assertEqual(len(context_recipes), 1)

    # category

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_status_code_404(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    # detail

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:detail', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_status_code_404(self):
        response = self.client.get(
            reverse('recipes:detail', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)
