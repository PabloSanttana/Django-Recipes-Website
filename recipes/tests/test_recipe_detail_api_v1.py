from django.urls import resolve, reverse

from recipes import views
from utils.utils_api import recipe_dict

from .test_recipe_base import RecipeTestBase

# Create your tests here.


class RecipeDetailApiV1Test(RecipeTestBase):
    def test_recipe_detail_api_v1_is_correct(self):
        view = resolve(
            reverse('recipes:details_v1_api', kwargs={'pk': 1})
        )
        self.assertIs(view.func.view_class, views.RecipeDetailViewApi)

    def test_recipe_detail_api_v1_status_code_404_Ok(self):
        response = self.client.get(
            reverse('recipes:details_v1_api', kwargs={'pk': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_api_v1_response_is_correct_recipe(self):
        # create recipes antes do template
        title = "this is a detail page - it load one recipe"
        create_recipe = self.make_recipe(title=title)
        response = self.client.get(
            reverse('recipes:details_v1_api', kwargs={'pk': 1})
        )

        recipe_to_dict = recipe_dict(self, create_recipe)

        # Verifica se a resposta HTTP foi bem-sucedida (código de status 200)
        self.assertEqual(response.status_code, 200)

        # Obtém os dados da resposta JSON
        data = response.json()['recipe']

        self.assertEqual(recipe_to_dict, data)

    def test_recipe_detail_api_v1_recipe_not_published(self):
        """
        Test if the Detail template correctly handles
        recipes that are not published.
        """

        self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:details_v1_api', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 404)
