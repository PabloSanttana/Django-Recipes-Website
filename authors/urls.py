from django.urls import path

from authors import views

app_name = "authors"

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.create_view, name='create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('dashboard/recipe/', views.dashboard_recipe_register,
         name='dashboard_recipe_register'),

    path('dashboard/recipe/create/', views.dashboard_recipe_create,
         name='dashboard_recipe_create'),

    path('dashboard/recipe/edit/<int:id>/', views.dashboard_recipe_edit,
         name='dashboard_recipe_edit'),
]
