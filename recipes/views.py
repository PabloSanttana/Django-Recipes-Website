from django.shortcuts import render
from django.http import HttpResponse
from recipes.models import Recipe, Category


# Create your views here.


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
        'title': 'Home'
    })


def category(request, id):
    recipes = Recipe.objects.filter(
        category__id=id,
        is_published=True
    ).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
        'title': recipes[0].category.name
    })


def recipe(request, id):
    recipe = Recipe.objects.filter(
        id=id,
        is_published=True
    ).order_by('-id').first()
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True
    })
