from django.views.generic.detail import DetailView

from recipes.models import Recipe


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/views/recipes_view.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        recipe = context_data.get('recipe')
        context_data.update({
            "is_detail_page": True,
            "title": f'{recipe.title} - Detail'
        })

        return context_data
