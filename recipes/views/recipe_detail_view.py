from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.views.generic.detail import DetailView

from recipes.models import Recipe
from utils.utils_api import recipe_dict


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/views/recipes_view.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)

        # fazendo relacoes de muitos para muitos
        queryset = queryset.select_related('author', 'category')
        queryset = queryset.prefetch_related('tags')

        if not queryset.exists():
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        recipe = context_data.get('recipe')
        context_data.update({
            "is_detail_page": True,
            "title": f'{recipe.title} - Detail'
        })

        return context_data


class RecipeDetailViewApi(RecipeDetailView):

    def render_to_response(self, context, **response_kwargs):

        context_data = self.get_context_data()
        recipe = context_data.get('recipe')
        # recipe_dict = model_to_dict(recipe)

        # if recipe_dict.get('cover'):
        #     recipe_dict['cover'] = self.request.build_absolute_uri()[0:21] + \
        #         recipe.cover.url
        # else:
        #     recipe_dict['cover'] = ""

        # if recipe.author.first_name is not None:
        # Flake8: noqa
        #     recipe_dict['author'] = f'{recipe.author.first_name} {recipe.author.last_name}'
        # else:
        #     recipe_dict['author'] = recipe.author.username

        # recipe_dict['category'] = str(recipe.category)

        # recipe_dict['created_at'] = str(recipe.created_at)
        # recipe_dict['updated_at'] = str(recipe.updated_at)

        # del recipe_dict['is_published']

        recipe_to_dict = recipe_dict(self, recipe)

        return JsonResponse({
            'recipe': recipe_to_dict,
        }, safe=False)
