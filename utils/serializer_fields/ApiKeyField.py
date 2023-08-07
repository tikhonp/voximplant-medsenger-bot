from django.conf import settings
from rest_framework import serializers


class ApiKeyField(serializers.CharField):
    """ApiKeyField for api key validation"""

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        if value != settings.APP_KEY:
            raise serializers.ValidationError('Invalid API key.')
        return value
