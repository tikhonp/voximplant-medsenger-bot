from django.conf import settings
from rest_framework.permissions import BasePermission


class ApiKeyPermission(BasePermission):
    """Medsenger agent request permission."""

    message = "`api_key` query param invalid or does not exists."
    MEDSENGER_APP_KEY = settings.MEDSENGER_APP_KEY

    def has_permission(self, request, view):
        api_key = request.query_params.get('api_key')
        return api_key == self.MEDSENGER_APP_KEY
