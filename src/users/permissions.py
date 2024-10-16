from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication


class IsActiveAuthenticated(BasePermission):
    def has_permission(self, request, view):
        jwt_auth = JWTAuthentication()
        try:
            user, _ = jwt_auth.authenticate(request)
            return user and user.is_active
        except jwt_auth.AuthenticationFailed:
            return False
