
from django.db.models import Q
from django.http import Http404, JsonResponse

from utils.utils_api import recipe_dict

from .recipe_list_view_base import RecipeListViewBase


class RecipeListHome(RecipeListViewBase):
    template_name = 'recipes/views/home.html'


class RecipeListHomeApi(RecipeListViewBase):
    template_name = 'recipes/views/home.html'

    def render_to_response(self, context, **response_kwargs):

        context_data = self.get_context_data()
        recipes = context_data.get('recipes')
        recipe_list = recipes.object_list.values()
        pagination_range = context_data.get('pagination_range')

        recipe_dict_list = []

        for recipe in recipes:
            item = recipe_dict(recipe)

            recipe_dict_list.append(item)

        return JsonResponse({
            # 'recipes': list(recipe_list),  # forma automatica do django
            'recipes': recipe_dict_list,
            'current_page': pagination_range['current_page'],
            'total_pages': pagination_range['total_pages'],
        }, safe=False)


class RecipeListCategory(RecipeListViewBase):
    template_name = 'recipes/views/category.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        category_id = self.kwargs.get('category_id')
        category_id
        queryset = queryset.filter(category__id=category_id)
        if not queryset.exists():
            raise Http404()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        recipes = context_data.get('recipes')
        category_name = ''

        if recipes:
            category_name = recipes[0].category.name

        context_data["title"] = f'{category_name}- Category'

        return context_data


class RecipeListSearch(RecipeListViewBase):
    template_name = 'recipes/views/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()

        if not search_term:
            raise Http404()

        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            ),
        )

        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()

        context_data.update({
            "page_title": f'{search_term}',
            "search_term": search_term,
            "additional_url_query": f'&q={search_term}'
        })

        return context_data
