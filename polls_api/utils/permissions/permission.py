from rest_framework.permissions import BasePermission

class Role:
    ADMIN = 1
    POLLSTER = 2
    POLLEE = 3
    
class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.groups.filter(id=Role.ADMIN).exists()

class IsPollster(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.groups.filter(id=Role.POLLSTER).exists()

class IsPollee(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.groups.filter(id=Role.POLLEE).exists()
