from django.db import models
from rest_framework import serializers


class CallRequestSerializer(serializers.Serializer):
    class Action(models.TextChoices):
        TEXT = 'TEXT'
        FINISH_CALL = 'FINISH_CALL'

    action = serializers.ChoiceField(choices=Action.choices)
    field = serializers.CharField(allow_blank=True)
