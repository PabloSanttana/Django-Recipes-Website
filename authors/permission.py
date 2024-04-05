from rest_framework import permissions


# verificar quem esta tentando fazer update ou delete e o dono do object
class IsAuthenticatedOrPostOnly(permissions.BasePermission):

    # obj retornar o model em questão
    def has_object_permission(self, request, view, obj):
        return obj == request.user

    def has_permission(self, request, view):
        # criar um usuario
        if request.method == 'POST':
            return True

        return request.user and request.user.is_authenticated
