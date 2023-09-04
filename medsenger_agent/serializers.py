from django.db import models
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from medsenger_agent.models import Contract
from utils.api_key_field import ApiKeyField


class ApiKeyBodySerializer(serializers.Serializer):
    api_key = ApiKeyField(write_only=True)


class ContractSerializer(ApiKeyBodySerializer):
    contract_id = serializers.IntegerField()
    patient_phone = PhoneNumberField(region='RU', read_only=True)
    patient_name = serializers.CharField(read_only=True)

    def create(self, validated_data):
        instance, created = Contract.objects.get_or_create(contract_id=validated_data.get('contract_id'))

        if not created:
            instance.is_active = True
            instance.save()

        return instance


class OrderSerializer(ApiKeyBodySerializer):
    class OrderChoices(models.TextChoices):
        USER_UPDATED = 'user_updated'
        NEW_TIMEZONE = 'new_timezone'

    contract_id = serializers.IntegerField()
    order = serializers.ChoiceField(choices=OrderChoices.choices)
