

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


class RecipeAPIViewListV2(APIView):
    def get(self, request, *args, **kwargs):
        recipes = Recipe.objects.get_published()[:10]
        #  many=True falando que são muitos
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        serializer = RecipeSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save(
            author_id=1,
            category_id=1,
            tags=[9, 12]
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class RecipeAPIViewDetailV2(APIView):
    def get_recipe(self, pk):
        recipe = get_object_or_404(
            Recipe.objects.get_published(),
            pk=pk,
        )
        return recipe

    def get(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={'request': request}
        )
        return Response(serializer.data)

    def patch(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            partial=True,
            many=False,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        recipe = self.get_recipe(pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def recipe_tag_api_v2(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk,
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request}
    )
    return Response(serializer.data)
