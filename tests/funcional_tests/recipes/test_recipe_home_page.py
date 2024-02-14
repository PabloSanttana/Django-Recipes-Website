
from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .test_base import RecipeBaseFunctionalTest


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

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_page_pagination(self):
        # Criar cinco receitas
        self.make_recipe_in_batch(5)

        # Usuário abre a página e verifica a paginação
        self.browser.get(self.live_server_url)

        # Verifica se há uma página 2
        page2 = self.browser.find_element(
            By.XPATH, '//a[@aria-label="Go to page 2"]')

        # Usuário clica na página 2 para ver as receitas daquela página
        page2.click()

        # Verifica se o usuário foi para a página 2
        current_page = self.browser.find_element(
            By.XPATH, '//a[@aria-label="Current page, 2"]')
        self.assertEqual('2', current_page.text)

        # Verifica se há mais duas receitas na página 2
        recipes = self.browser.find_elements(By.CLASS_NAME, 'recipe-list-item')
        self.assertEqual(2, len(recipes))
