from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Чтение разрешено всем
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Изменение — только админам
        return request.user and request.user.is_staff


class NotAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_authenticated

    
