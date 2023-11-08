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
        # create recipes antes do template
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


class RecipeViewDetailTest(RecipeTestBase):
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


class RecipeViewCategoryTest(RecipeTestBase):
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

    def test_recipe_category_template_loads_the_correct_recipes(self):
        # create recipes antes do template
        title = "This is a category test"
        create_recipe = self.make_recipe(title=title)
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1})
        )

        recipes = response.context["recipes"]
        recipes
        # usando context
        self.assertEqual(len(recipes), 1)
        self.assertEqual(create_recipe.title, recipes[0].title)

        # usando content
        content = response.content.decode('utf-8')

        self.assertIn(title, content)
        self.assertIn('sanatana', content)
        self.assertIn('carnes', content)
