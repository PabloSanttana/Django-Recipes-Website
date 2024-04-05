

from django.contrib.auth import get_user_model
from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authors.permission import IsAuthenticatedOrPostOnly
from authors.serializer import AuthorSerializer


class AuthorAPIV2CRUDViewSet(ModelViewSet):
    serializer_class = AuthorSerializer

    permission_classes = [IsAuthenticatedOrPostOnly]

    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.filter(username=self.request.user.username)

        return qs

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_queryset().first()
        serializer = AuthorSerializer(
            instance=user,
            data=request.data,
            partial=True,
            many=False,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
