from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase

# Create your tests here.


class RecipeViewSearchTest(RecipeTestBase):

    def test_recipe_search_view_is_correct(self):
        view = resolve(
            reverse("recipes:search")
        )
        self.assertIs(view.func, views.search)

    def test_recipe_search_view_loads_correct_template(self):
        url = reverse('recipes:search') + "?q=carnes"
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/views/search.html')

    def test_recipe_search_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + "?q=carnes"
        response = self.client.get(url)
        self.assertIn('Search for carnes', response.content.decode('utf-8'))
