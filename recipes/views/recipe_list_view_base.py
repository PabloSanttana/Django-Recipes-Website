
import os

from django.views.generic import ListView

from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 9))


class RecipeListViewBase(ListView):
    # allow_empty = True
    # queryset = None
    model = Recipe
    paginate_by = None
    # paginate_orphans = 0
    context_object_name = 'recipes'
    # paginator_class = Paginator
    # page_kwarg = "page"
    ordering = ['-id']
    template_name = 'recipes/views/home.html'

    # fazer os filtros

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            is_published=True
        )
        return queryset

    def get_context_data(self,  *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        page_obj, pagination_range = make_pagination(
            self.request,
            context_data.get('recipes'),
            PER_PAGE
        )

        context_data.update({
            'recipes': page_obj,
            "pagination_range": pagination_range
        })

        return context_data
