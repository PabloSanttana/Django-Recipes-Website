from io import BytesIO

from django.contrib.auth.models import User
from PIL import Image

from recipes.models import Category, Recipe


class AuthorsMixin:
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

    def make_recipe(self,
                    title='Classic Spaghetti Carbonara',
                    is_published=False,
                    user=None,
                    ):

        try:
            category = Category.objects.get(name='Carnes')
        except Category.DoesNotExist:
            # Se a categoria não existir, crie-a
            category = Category.objects.create(name='Carnes')

        return Recipe.objects.create(
            title=title,
            description='A traditional Italian',
            preparation_time='30',
            preparation_time_unit='Minutos',
            servings='4',
            servings_unit='Porçōes',
            preparation_steps='1. Cook spaghetti according ',
            preparation_steps_is_html=False,
            is_published=is_published,
            category=category,
            author=user,
        )
