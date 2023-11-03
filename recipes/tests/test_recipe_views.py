from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views

# Create your tests here.


class RecipeViewHomeTest(TestCase):
    def test_recipe_home_view_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_status_code_200_Ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/views/home.html')

    def test_recipe_home_template_shows_not_recipes_found_if_no_recipe(self):
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        text = "<h2 >Atualmente, não temos nenhuma receita publicada.</h2>"
        self.assertIn(text, content)


class RecipeViewDetailTest(TestCase):
    def test_recipe_detail_view_is_correct(self):
        view = resolve(
            reverse('recipes:details', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.recipes)

    def test_recipe_detail_view_status_code_404_Ok(self):
        response = self.client.get(
            reverse('recipes:details', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)


class RecipeViewCategoryTest(TestCase):
    def test_recipe_category_view_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_status_code_404_Ok(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)
