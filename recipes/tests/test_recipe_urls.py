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
        url = reverse('recipes:details', kwargs={'id': 1})
        self.assertEqual(url, "/recipes/1/")
