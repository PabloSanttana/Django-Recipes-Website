from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def make_category(self, name="carnes"):
        return Category.objects.create(name=name)

    def make_author(self,
                    first_name="pablo",
                    last_name="sanatana",
                    username="guilherme",
                    password="pablo@1234",
                    email="guilherme@example.com"
                    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email
        )

    def make_recipe(self,
                    title="title",
                    description="description",
                    slug="title-one",
                    preparation_time=10,
                    preparation_time_unit="minute",
                    servings=10,
                    servings_unit="pessoas",
                    preparation_steps="preparation_steps",
                    preparation_steps_is_html=False,
                    is_published=True,
                    category_data=None,
                    author_data=None

                    ):

        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            category=self.make_category(**category_data),
            author=self.make_author(**author_data)
        )
