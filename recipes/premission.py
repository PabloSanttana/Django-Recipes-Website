from rest_framework import permissions


# verificar quem esta tentando fazer update ou delete e o dono do object
class isOwner(permissions.BasePermission):

    # obj retornar o model em questão
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

    def has_permission(self, request, view):
        return super().has_permission(request, view)
