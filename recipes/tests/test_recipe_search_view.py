from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase

# Create your tests here.


class RecipeViewSearchTest(RecipeTestBase):

    def test_recipe_search_view_is_correct(self):
        view = resolve(
            reverse("recipes:search")
        )
        self.assertIs(view.func.view_class, views.RecipeListSearch)

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

    def test_recipe_search_can_find_recipe_by_title(self):
        title_one = "This is recipe one"
        title_two = "This is recipe two"

        recipe_one = self.make_recipe(
            slug="recipe-one",
            title=title_one,
            author_data={'username': 'one'}
        )
        recipe_two = self.make_recipe(
            slug="recipe-two",
            title=title_two,
            author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response_one = self.client.get(f'{search_url}?q={title_one}')
        response_two = self.client.get(f'{search_url}?q={title_two}')
        response_both = self.client.get(f'{search_url}?q=This')

        self.assertIn(recipe_one, response_one.context['recipes'])
        self.assertNotIn(recipe_two, response_one.context['recipes'])

        self.assertIn(recipe_two, response_two.context['recipes'])
        self.assertNotIn(recipe_one, response_two.context['recipes'])

        self.assertIn(recipe_one, response_both.context['recipes'])
        self.assertIn(recipe_two, response_both.context['recipes'])
