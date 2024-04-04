

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


@api_view()
def recipe_list_api_v2(request):
    recipes = Recipe.objects.get_published()[:10]
    #  many=True falando que são muitos
    serializer = RecipeSerializer(instance=recipes, many=True)
    return Response(serializer.data)


@api_view()
def recipe_detail_api_v2(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk,
    )
    serializer = RecipeSerializer(instance=recipe, many=False)
    return Response(serializer.data)
