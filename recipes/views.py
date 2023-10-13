from django.http import HttpResponse
from django.shortcuts import render


def home_view(request):
    return render(request, 'recipes/pages/home.html', {
        "name": "TE AMO MUITO!! :)"
    })


def sobre_url(request):
    return HttpResponse("Home")


def contato_url(request):
    return HttpResponse("Home")

# Create your views here.
