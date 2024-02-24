from io import BytesIO
from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized
from PIL import Image

from authors.forms import RecipeForm
from recipes.models import Category, User


class AuthorCreateRecipeFormUnitTest(TestCase):
    @parameterized.expand([
        ('title', 'Recipe title'),
        ('description', 'Recipe description'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder_value):
        form = RecipeForm()
        placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder_value, placeholder)

    @parameterized.expand([
        ('is_published'),
        ('slug'),
        ('author'),
        ('preparation_steps_is_html'),
    ])
    def test_fields_removed_from_the_form_is_correct(self, field):
        form = RecipeForm()
        fields = form.fields.keys()
        self.assertNotIn(field, fields)

    @parameterized.expand([
        ('title', 'The recipe title must have at least 5 characters.'),
        ('description', ('The recipe description must have at least 5 '
                         'characters.')),
        ('preparation_steps', ('The field accepts both plain text and HTML '
                               'format for better organization.')),
        ('cover', ('Accepted files jpg, jpeg, png '
                   'with a maximum size of 2MB.')),
    ])
    def test_fields_help_text_is_corrects(self, field, help_text_value):
        form = RecipeForm()
        help_text = form[field].field.help_text
        self.assertEqual(help_text_value, help_text)

    @parameterized.expand([
        ('servings_unit', [('Porçōes', 'Porçōes'),
                          ('Pedaços', 'Pedaços'),
                           ('Pessoas', 'Pessoas')]),
        ('preparation_time_unit', [('Horas', 'Horas'),
                                   ('Minutos', 'Minutos'),]),
    ])
    def test_fields_with_choices_is_correct(self, field, choices_value):
        form = RecipeForm()
        choices = form[field].field.widget.choices

        self.assertEqual(choices_value, choices)


class AuthorCreateRecipeFormIntegrationTestCase(DjangoTestCase):

    def setUp(self, *args, **kwargs) -> None:

        self.make_login_author()
        category = Category.objects.create(name='Pasta')

        image = self.generate_photo_file()
        self.form_data = {
            'title': 'Classic Spaghetti Carbonara',
            'description': ('A traditional Italian '
                            'pasta dish made with eggs.'),
            'preparation_time': '30',
            'preparation_time_unit': 'Minutos',
            'servings': '4',
            'servings_unit': 'Porçōes',
            'preparation_steps': ('1. Cook spaghetti according '
                                  'to package instructions.'),
            'cover': image,
            'category': category.id
        }

        return super().setUp()

    def generate_photo_file(self,  additional_bytes=1000, format_file="png"):
        # Criar um objeto BytesIO para armazenar o conteúdo na memória
        file_obj = BytesIO()

        # Criar uma nova imagem com o tamanho especificado e um fundo vermelho
        image = Image.new("RGBA", size=(50, 50), color=(256, 0, 0))

        # Salvar a imagem no objeto BytesIO no formato PNG
        image.save(file_obj, format_file)

        # Definir o nome do arquivo (opcional)
        file_obj.name = f'arquivoFile.{format_file}'

        # Calcular o tamanho atual do arquivo
        current_size = len(file_obj.getvalue())

        # Calcular o tamanho total desejado do arquivo
        # (incluindo os bytes adicionais)
        desired_size = current_size + additional_bytes

        # Adicionar bytes extras para atingir o tamanho desejado
        if desired_size > current_size:
            file_obj.write(b'0' * (desired_size - current_size))

        # Definir o tamanho do arquivo
        file_obj.size = len(file_obj.getvalue())

        # Voltar para o início do arquivo para que ele possa ser lido novamente
        file_obj.seek(0)

        # Retornar o objeto BytesIO contendo a imagem gerada
        return file_obj

    def make_create_author(self):
        # cria um usuario
        self.user_password = 'Ab123456789'
        user = User.objects.create_user(
            username='RafaelaDarc',
            last_name='Darc',
            first_name='Rafaela',
            email='RafaelaDarc@gmail.com',
            password=self.user_password)
        return user

    def make_login_author(self):
        user = self.make_create_author()
        self.client.login(username=user.username, password=self.user_password)
        return user

    @parameterized.expand([
        ('title', 'This field must not be empty.'),
        ('description', 'This field must not be empty.'),
        ('preparation_time', 'This field must not be empty.'),
        ('preparation_time_unit', 'This field must not be empty.'),
        ('servings', 'This field must not be empty.'),
        ('servings_unit', 'This field must not be empty.'),
        ('preparation_steps', 'This field must not be empty.'),
        ('category', 'Category is required.'),
        ('cover', 'Cover image is required.'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        post_url = reverse('authors:dashboard_recipe_new')
        response = self.client.post(
            post_url, data=self.form_data,
            format="multipart/form-data", follow=True)

        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_field_cover_size_not_exceed_2MB(self):

        image = self.generate_photo_file(additional_bytes=3 * 1024 * 1024)

        self.form_data['cover'] = image
        post_url = reverse('authors:dashboard_recipe_new')
        response = self.client.post(
            post_url, data=self.form_data,
            format="multipart/form-data", follow=True)

        self.assertIn("Cover image should not exceed 2MB",
                      response.context['form'].errors.get('cover'))

    def test_filed_cover_format_not_invalid(self):

        image = self.generate_photo_file(format_file='pdf')

        self.form_data['cover'] = image
        post_url = reverse('authors:dashboard_recipe_new')
        response = self.client.post(
            post_url, data=self.form_data,
            format="multipart/form-data", follow=True)
        msg = ('Envie uma imagem válida. O arquivo enviado '
               'não é uma imagem ou está corrompido.')
        self.assertIn(msg,
                      response.context['form'].errors.get('cover'))

    @parameterized.expand([
        ('preparation_time', 'Preparation time must be a positive number.'),
        ('servings', 'Servings must be a positive number.'),
    ])
    def test_fields_must_be_positiver_number(self, field, msg):
        self.form_data[field] = -10
        post_url = reverse('authors:dashboard_recipe_new')
        response = self.client.post(
            post_url, data=self.form_data,
            format="multipart/form-data", follow=True)

        self.assertIn(msg,
                      response.context['form'].errors.get(field))

    @parameterized.expand([
        ('title', 'Title must have at least 5 characters.'),
        ('description', 'Description must have at least 5 characters.'),
    ])
    def test_fields_min_length(self, field, msg):
        self.form_data[field] = "aaa"

        post_url = reverse('authors:dashboard_recipe_new')
        response = self.client.post(
            post_url, data=self.form_data,
            format="multipart/form-data", follow=True)

        self.assertIn(msg,
                      response.context['form'].errors.get(field))

    def test_recipe_form_successfully_submitted(self):

        post_url = reverse('authors:dashboard_recipe_new')
        response = self.client.post(
            post_url, data=self.form_data,
            format="multipart/form-data", follow=True)

        msg = 'Recipe form successfully submitted.'
        self.assertIn(msg, response.content.decode('utf-8'))
