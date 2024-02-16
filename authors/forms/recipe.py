from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
