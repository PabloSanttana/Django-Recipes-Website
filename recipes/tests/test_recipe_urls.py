from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class RecipeURLsTestCase(TestCase):
    def test_recipe_home_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, "/")

    def test_recipe_category_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, "/recipes/category/1/")

    def test_recipe_detail_is_correct(self):
        url = reverse('recipes:details', kwargs={'pk': 1})
        self.assertEqual(url, "/recipes/1/")

    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, "/recipes/search/")


class RecipeURLsApiTestCase(TestCase):
    def test_recipe_home_api_v1_is_correct(self):
        url = reverse('recipes:home_v1_api')
        self.assertEqual(url, "/recipes/api/v1/")

    def test_recipe_detail_api_v1_is_correct(self):
        url = reverse('recipes:details_v1_api', kwargs={'pk': 1})
        self.assertEqual(url, "/recipes/api/v1/1/")
