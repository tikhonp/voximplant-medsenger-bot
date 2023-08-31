from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied


class ApiKeyField(serializers.CharField):
    """ApiKeyField for api key validation."""

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        if value != settings.MEDSENGER_APP_KEY:
            raise PermissionDenied('Invalid API key.')
        return value
