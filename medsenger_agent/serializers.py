from rest_framework import serializers

from medsenger_agent.models import Contract
from utils.serializer_fields.api_key_field import ApiKeyField


class ApiKeyBodySerializer(serializers.Serializer):
    api_key = ApiKeyField(write_only=True)


class ContractSerializer(ApiKeyBodySerializer):
    contract_id = serializers.IntegerField()

    def create(self, validated_data):
        instance, created = Contract.objects.get_or_create(contract_id=validated_data.get('contract_id'))

        if not created:
            instance.is_active = True
            instance.save()

        return instance
