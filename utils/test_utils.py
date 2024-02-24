from django.test import TestCase

from recipes.tests.test_recipe_base import RecipeMixin
from utils.django_forms import is_positive_number
from utils.utils_api import recipe_dict


class ApiDictTestCase(TestCase, RecipeMixin):

    def teste_is_convert_recipe_dict(self):
        recipe = self.make_recipe()
        dict_recipe = recipe_dict(self, recipe)

        self.assertEqual(recipe.id, dict_recipe['id'])
        self.assertEqual(recipe.title, dict_recipe['title'])
        self.assertEqual(recipe.author.username,
                         dict_recipe['author']['username'])

        self.assertEqual("", dict_recipe['cover']['url'])


class TestFunctionUtilsAll(TestCase):

    def test_function_is_positive_number(self):
        self.assertFalse(is_positive_number('AA'))
        self.assertTrue(is_positive_number(10))
        self.assertFalse(is_positive_number(-10))
