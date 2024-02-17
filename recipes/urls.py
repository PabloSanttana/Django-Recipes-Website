from django.urls import path

from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListHome.as_view(), name='home'),
    path('recipes/search/', views.RecipeListSearch.as_view(), name='search'),
    path('recipes/category/<int:category_id>/',
         views.RecipeListCategory.as_view(), name='category'),
    path('recipes/<int:pk>/',
         views.RecipeDetailView.as_view(), name='details'),
]
