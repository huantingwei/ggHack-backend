from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view and edit it.
    """        
    def has_object_permission(self, request, view, obj):
        # all methods should be protected  
        
        return obj.owner == request.user

class IsCustomer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # all methods should be protected

        return obj.customer == request.user


class IsProvider(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # all methods should be protected
        return obj.serviceOwner == request.user