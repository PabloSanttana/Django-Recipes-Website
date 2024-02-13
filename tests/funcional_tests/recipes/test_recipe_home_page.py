
from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomeFunctionTestCase(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_no_recipes_published(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn(
            'Atualmente, não temos nenhuma receita publicada.', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        # criar as receitas
        recipes = self.make_recipe_in_batch(5)

        title_needed = 'This is whats I need'
        recipes[0].title = title_needed
        recipes[0].save()

        # emular uma busca de uma recieta pelo title
        self.browser.get(self.live_server_url)

        # selecionar o campo
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search..."]'
        )

        # clica neste input e digitar o termo de busca
        # para encontrar a receita com o titulo desejado

        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # o usuario ver oque estava procurando na pagina
        content_title = self.browser.find_element(
            By.CLASS_NAME, 'recipe-title')

        self.assertIn(title_needed, content_title.text)
