from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase

# Create your tests here.


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
            reverse('recipes:category', kwargs={
                    'category_id': create_recipe.category.id})
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

    def test_recipe_category_template_recipes_not_published(self):
        """
        Test if the category template correctly handles
        recipes that are not published.
        """

        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category', kwargs={
                    'category_id': recipe.category.id})
        )
        self.assertEqual(response.status_code, 404)
