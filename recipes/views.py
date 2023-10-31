from django.shortcuts import get_list_or_404, get_object_or_404, render

from recipes.models import Recipe

# from utils.factory import make_recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by("-id")
    return render(request, 'recipes/views/home.html', {
        "recipes": recipes
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True
        ).order_by("-id")
    )

    return render(request, 'recipes/views/category.html', {
        "recipes": recipes,
        "title": f'{recipes[0].category.name}- Category'
    })


def recipes(request, id):
    recipe = get_object_or_404(Recipe, pk=id,  is_published=True)

    return render(request, 'recipes/views/recipes_view.html', {
        "recipe": recipe,
        "is_detail_page": True,
        "title": f'{recipe.title} - Detail'
    })
