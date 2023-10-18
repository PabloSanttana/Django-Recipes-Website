from django.shortcuts import render

from utils.factory import make_recipe


def home(request):
    return render(request, 'recipes/views/home.html', {
        "recipes": [make_recipe() for _ in range(10)]
    })


def recipes(request, id):
    return render(request, 'recipes/views/recipes_view.html', {
        "recipe": make_recipe(),
        "is_detail_page": True
    })
