from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from recipes import views

app_name = 'recipes'

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register(
    'recipes/api/v2',
    views.RecipeAPIv2CRUDViewSet,
    basename='recipes-api',
)

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
        'recipes/api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'recipes/api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'recipes/api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),

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


    path('', include(recipe_api_v2_router.urls)),

    path(
        'recipes/api/v2/tag/<int:pk>/',
        views.recipe_tag_api_v2,
        name='recipes_tag_api_v2'
    ),

]
