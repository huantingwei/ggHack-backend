from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view and edit it.
    """        
    def has_object_permission(self, request, view, obj):
        # all methods should be protected
        try:
            owner = obj.owner
        except AttributeError:
            return obj.customer == request.user      
        
        return owner == request.user
