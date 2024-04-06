

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipes.models import Recipe
from recipes.premission import isOwner
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
    permission_classes = [IsAuthenticatedOrReadOnly,]
    http_method_names = ['get', 'post', 'patch', 'options', 'head', 'delete']

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

    def get_object(self):
        pk = self.kwargs.get('pk', '')

        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )
        # Verificar nossa funcao de permissao 'permission.py'
        self.check_object_permissions(self.request, obj)

        return obj

    # metodo da super class
    # estamos reescrevendo
    def get_permissions(self):
        # se o metodo for algum desse chame a nossa permissão
        if self.request.method in ['PATCH', 'DELETE']:
            return [isOwner(), ]
        return super().get_permissions()

    # sobreescrevendo essa função como exemplo
    # dps refazer isso para atualizar a recita nao deve esta publidad
    def partial_update(self, request, *args, **kwargs):
        recipe = self.get_object()
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

    def list(self, request, *args, **kwargs):
        print('REQUEST', request.user)
        print(request.user.is_authenticated)
        return super().list(request, *args, **kwargs)

    # Metdo para cria uma recita

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category_id = request.data.get('category')

        serializer.save(
            author=request.user,
            category_id=category_id
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


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
