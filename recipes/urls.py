from django.urls import path

from recipes.views import home_view

urlpatterns = [
    path('', home_view)
]
