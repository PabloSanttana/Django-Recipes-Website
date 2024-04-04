from django.urls import path

from recipes import views

app_name = 'recipes'

urlpatterns = [
    path(
        '',
        views.RecipeListHome.as_view(),
        name='home'
    ),
    path(
        'recipes/search/',
        views.RecipeListSearch.as_view(),
        name='search'
    ),
    path(
        'recipes/tags/<slug:slug>/',
        views.RecipeListTag.as_view(),
        name='tag'
    ),

    path(
        'recipes/category/<int:category_id>/',
        views.RecipeListCategory.as_view(),
        name='category'
    ),
    path(
        'recipes/<int:pk>/',
        views.RecipeDetailView.as_view(),
        name='details'
    ),


    # Rotas de Api começam aqui sem usar django rest framework
    path(
        'recipes/api/v1/',
        views.RecipeListHomeApi.as_view(),
        name='home_v1_api'
    ),
    path(
        'recipes/api/v1/<int:pk>/',
        views.RecipeDetailViewApi.as_view(),
        name='details_v1_api'
    ),

    # Rotas de Api v2 usando django rest framework

    path(
        'recipes/api/v2/',
        views.recipe_list_api_v2,
        name='recipes_v2_api'
    ),
    path(
        'recipes/api/v2/<int:pk>/',
        views.recipe_detail_api_v2,
        name='recipes_detail_v2_api'
    ),
    path(
        'recipes/api/v2/tag/<int:pk>/',
        views.recipe_tag_api_v2,
        name='recipes_tag_api_v2'
    ),

]
