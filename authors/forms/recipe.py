from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr, is_positive_number


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # criar um dicionario dinamico para armazenar os errors de uma vez
        self.__my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        add_attr(self.fields.get('title'), 'class', 'span-2')
        add_attr(self.fields.get('description'), 'class', 'span-2')

    class Meta:
        model = Recipe
        exclude = ['is_published', 'slug',
                   'author', 'preparation_steps_is_html']

        widgets = {
            'cover': forms.FileInput(
                attrs={'class': 'span-2'}
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porçōes', 'Porçōes'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Horas', 'Horas'),
                    ('Minutos', 'Minutos'),
                )
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.cleaned_data

        # Verifica se a descrição tem pelo menos 5 caracteres
        if len(cleaned_data.get('description', '')) < 5:
            self.__my_errors['description'].append(
                'Description must have at least 5 characters.')

        # Verifica se o tempo de preparo é um número positivo
        if not is_positive_number(cleaned_data.get('preparation_time', 0)):
            self.__my_errors['preparation_time'].append(
                'Preparation time must be a positive number.')

        # Verifica se o número de porções é um número positivo
        if not is_positive_number(cleaned_data.get('servings', 0)):
            self.__my_errors['servings'].append(
                'Servings must be a positive number.')

        # Verifica se a imagem de capa está presente
        if not cleaned_data.get('cover'):
            self.__my_errors['cover'].append(
                'Cover image is required')

        # Verifica se a categoria está presente
        if not cleaned_data.get('category'):
            self.__my_errors['category'].append(
                'Category is required')

        # Se houver erros, lança uma exceção de validação
        if self.__my_errors:
            raise ValidationError(self.__my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title', '')

        # Verifica se o título tem pelo menos 5 caracteres
        if len(title) < 5:
            self.__my_errors['title'].append(
                'Ttile must have at least 5 characters.')

        return title
