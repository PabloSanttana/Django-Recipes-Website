from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase

# Create your tests here.


class RecipeViewDetailTest(RecipeTestBase):
    def test_recipe_detail_view_is_correct(self):
        view = resolve(
            reverse('recipes:details', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_status_code_404_Ok(self):
        response = self.client.get(
            reverse('recipes:details', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_load_is_correct_recipe(self):
        # create recipes antes do template
        title = "this is a detail page - it load one recipe"
        create_recipe = self.make_recipe(title=title)
        response = self.client.get(
            reverse('recipes:details', kwargs={'id': 1})
        )

        recipe = response.context["recipe"]
        # usando context
        self.assertEqual(create_recipe.title, recipe.title)

        # usando content
        content = response.content.decode('utf-8')

        self.assertIn(title, content)
        self.assertIn('sanatana', content)

    def test_recipe_detail_template_recipe_not_published(self):
        """
        Test if the Detail template correctly handles
        recipes that are not published.
        """

        self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:details', kwargs={'id': 1})
        )
        self.assertEqual(response.status_code, 404)
