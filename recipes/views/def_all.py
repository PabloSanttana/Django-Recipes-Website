
import os

from django.db.models import Q
from django.shortcuts import (Http404, get_list_or_404, get_object_or_404,
                              render)

from recipes.models import Recipe
from utils.pagination import make_pagination

# from utils.factory import make_recipe

PER_PAGE = int(os.environ.get('PER_PAGE', 9))


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by("-id")

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/views/home.html', {
        "recipes": page_obj,
        "pagination_range": pagination_range
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True
        ).order_by("-id")
    )

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/views/category.html', {
        "recipes": page_obj,
        "pagination_range": pagination_range,
        "title": f'{recipes[0].category.name}- Category'
    })


def recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk,  is_published=True)

    return render(request, 'recipes/views/recipes_view.html', {
        "recipe": recipe,
        "is_detail_page": True,
        "title": f'{recipe.title} - Detail'
    })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True).order_by("-id")

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/views/search.html', {
        "page_title": f'{search_term}',
        "search_term": search_term,
        "recipes": page_obj,
        "pagination_range": pagination_range,
        "additional_url_query": f'&q={search_term}'
    })
