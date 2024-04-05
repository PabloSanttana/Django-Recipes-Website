

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag

RECIPE_PAGE_SIZE = 10


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = RECIPE_PAGE_SIZE
    page_size_query_param = 'page_size'


# faz o crud completo
class RecipeAPIv2CRUDViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination

    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get('category_id', '')
        search_term = self.request.query_params.get('q', '').strip()

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        if search_term != '':
            qs = qs.filter(
                Q(
                    Q(title__icontains=search_term) |
                    Q(description__icontains=search_term)
                ),
            )

        return qs

    # sobreescrevendo essa função como exemplo

    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        recipe = self.get_queryset().filter(pk=pk).first()
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
