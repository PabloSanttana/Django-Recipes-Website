from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from recipes.models import Recipe
from utils.pagination import make_pagination

# versao em classe da def dashboard


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch')
class DashboardRecipeListView(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'authors/views/dashboard.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            is_published=False,
            author=self.request.user
        ).values('id', 'title', 'created_at')

        return queryset

    def get_context_data(self,  *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        recipes = context_data.get('recipes')
        total_recipes = len(recipes)
        page_obj, pagination_range = make_pagination(
            self.request,
            recipes,
            10
        )
        html_language = translation.get_language()
        context_data.update({
            'recipes': page_obj,
            "pagination_range": pagination_range,
            'total_recipes': total_recipes,
            'html_language': html_language
        })
        return context_data
