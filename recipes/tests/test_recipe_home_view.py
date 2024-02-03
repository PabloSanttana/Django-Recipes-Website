from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase

# Create your tests here.


class RecipeViewHomeTest(RecipeTestBase):
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

    def test_recipe_home_template_loads_recipes(self):
        # criar receitas ante de chama a view
        create_recipe = self.make_recipe(author_data={
            'first_name': 'Pablo'
        })
        response = self.client.get(reverse('recipes:home'))

        recipes = response.context["recipes"]

        # usando context
        self.assertEqual(len(recipes), 1)
        self.assertEqual(create_recipe.title, recipes[0].title)

        # usando content
        content = response.content.decode('utf-8')
        self.assertIn(create_recipe.title, content)
        self.assertIn('Pablo', content)

    def test_recipe_home_template_recipes_not_published(self):
        """
        Test if the home template correctly handles
        recipes that are not published.
        """

        # Criar receitas antes de chamar a view
        self.make_recipe(is_published=False)

        # Chamar a view
        response = self.client.get(reverse('recipes:home'))

        recipes = response.context["recipes"]
        # Verifica se a chave 'recipes' não está presente no contexto
        self.assertEqual(len(recipes), 0)

        # Verificar se o código de status é 200 (OK)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        text = "<h2 >Atualmente, não temos nenhuma receita publicada.</h2>"
        self.assertIn(text, content)

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_is_pagination(self):
        # testando paginacao da home

        for i in range(9):
            kwargs = {'slug': f'slug-{i}',
                      'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(3)), 3)
