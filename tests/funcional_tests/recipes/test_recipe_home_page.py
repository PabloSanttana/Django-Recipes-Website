
from selenium.webdriver.common.by import By

from .base import RecipeBaseFunctionalTest


class RecipeHomeFunctionTestCase(RecipeBaseFunctionalTest):

    def test_recipe_home_page_no_recipes_published(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn(
            'Atualmente, não temos nenhuma receita publicada.', body.text)
