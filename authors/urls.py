from django.urls import path

from authors import views

app_name = "authors"

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.create_view, name='create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),

    # path('dashboard/', views.dashboard, name='dashboard'),


    path('dashboard/', views.DashboardRecipeListView.as_view(),
         name='dashboard'),
    path('dashboard/recipe/new/', views.DashboardRecipe.as_view(),
         name='dashboard_recipe_new'),

    path('dashboard/recipe/delete', views.DashboardRecipeDelete.as_view(),
         name='dashboard_recipe_delete'),

    path('dashboard/recipe/edit/<int:id>/', views.DashboardRecipe.as_view(),
         name='dashboard_recipe_edit'),
]
