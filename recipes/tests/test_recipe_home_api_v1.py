from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase

# Create your tests here.


class RecipeHomeApiV1Test(RecipeTestBase):
    def test_recipe_home_api_v1_is_correct(self):
        view = resolve(reverse('recipes:home_v1_api'))

        self.assertIs(view.func.view_class, views.RecipeListHomeApi)

    def test_recipe_home_api_v1_status_code_200_Ok(self):
        response = self.client.get(reverse('recipes:home_v1_api'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_api_v1_not_recipes(self):
        response = self.client.get(reverse('recipes:home_v1_api'))
        data = response.json()['recipes']
        self.assertEqual(0, len(data))

    def test_recipe_home_api_v1_response_recipes(self):
        # criar receitas ante de chama a view
        create_recipe = self.make_recipe(author_data={
            'first_name': 'Pablo'
        })
        response = self.client.get(reverse('recipes:home_v1_api'))
        data = response.json()['recipes']

        data
        # usando context
        self.assertEqual(len(data), 1)
        self.assertEqual(create_recipe.title, data[0]['title'])
        self.assertEqual('Pablo', data[0]['author']['first_name'])

    def test_recipe_home_api_v1_recipes_not_published(self):
        """
        Test if the home template correctly handles
        recipes that are not published.
        """

        # Criar receitas antes de chamar a view
        self.make_recipe(is_published=False)

        # Chamar a api
        response = self.client.get(reverse('recipes:home_v1_api'))

        data = response.json()['recipes']
        # Verifica se a chave 'recipes' não está presente no contexto
        self.assertEqual(len(data), 0)

        # Verificar se o código de status é 200 (OK)
        self.assertEqual(response.status_code, 200)

    # @patch('recipes.views.PER_PAGE', new=3)

    @patch('recipes.views.recipe_list_view_base.PER_PAGE', new=3)
    def test_recipe_home_api_v1_is_pagination_page_query_invalid(self):

        for i in range(9):
            kwargs = {'slug': f'slug-{i}',
                      'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        response = self.client.get(reverse('recipes:home_v1_api')+'?page=2A')
        data = response.json()

        data

        self.assertEqual(data['current_page'], 1)
        self.assertEqual(data['total_pages'], 3)
