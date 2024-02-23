from django.core.exceptions import ValidationError
from django.urls import reverse
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_default(self):
        recipe = Recipe(
            title="title recipe",
            description="description",
            preparation_time=10,
            preparation_time_unit="minute",
            servings=10,
            servings_unit="pessoas",
            preparation_steps="preparation_steps",
            category=self.make_category(name='Peixe'),
            author=self.make_author(username="maciel")
        )

        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()

        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg="Recipe preparation_steps_is_html is not false"
        )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(
            recipe.is_published,
            msg="Recipe is_published is not false"
        )

    def test_recipe_string_representation(self):
        needed = "Testing Representation"
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), needed)

    def test_recipe_save_method_generates_unique_slug_for_new_object(self):
        title = "Testing recipe"
        self.recipe.title = title
        self.recipe.full_clean()
        self.recipe.save()
        slug = self.recipe.slug
        self.assertIn("testing-recipe", slug)
    # Flake8: noqa

    def test_recipe_save_method_generates_unique_slug_when_title_is_changed(self):
        # Criar um objeto Recipe existente
        self.recipe.title = 'Test Recipe'
        self.recipe.full_clean()
        self.recipe.save()

        # Modificar o título
        self.recipe.title = 'Modified Test Recipe'
        self.recipe.full_clean()
        self.recipe.save()

        # Verificar se o slug foi atualizado
        self.assertIn('modified-test-recipe', self.recipe.slug)

    def test_recipe_save_method_not_modified_Modified(self):
        self.recipe.title = 'New Title Recipe'
        self.recipe.full_clean()
        self.recipe.save()

        self.recipe.description = "Modified description"
        self.recipe.full_clean()
        self.recipe.save()

        # verificar se o slug nao foi modificado
        self.assertIn('new-title-recipe', self.recipe.slug)

    def test_recipe_is_correct_get_absolute_url(self):
        url = reverse('recipes:details', kwargs={"pk": self.recipe.id})
        self.assertEqual(url, self.recipe.get_absolute_url())
