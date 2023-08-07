from rest_framework import serializers

from forms.serializers import FormSerializer, TimeSlotSerializer
from medsenger_agent.models import Contract
from utils.serializer_fields import ApiKeyField


class ContractCreateSerializer(serializers.Serializer):
    api_key = ApiKeyField
    contract_id = serializers.IntegerField()

    def save(self):
        instance, created = Contract.objects.get_or_create(contract_id=self.validated_data.get('contract_id'))

        if not created:
            instance.is_active = True
            instance.save()

        return instance


class ContractRemoveSerializer(serializers.Serializer):
    api_key = ApiKeyField
    contract_id = serializers.IntegerField()


class StatusSerializer(serializers.Serializer):
    api_key = ApiKeyField


class SettingsFormSerializer(serializers.Serializer):
    form_id = serializers.IntegerField()


class SettingsTimeSlotSerializer(serializers.Serializer):
    time = serializers.TimeField()


class ContractSerializer(serializers.Serializer):
    contract_id = serializers.IntegerField()
    forms = serializers.ListSerializer(child=FormSerializer(), source='form_set')
    time_slots = serializers.ListSerializer(child=TimeSlotSerializer(), source='time_slot_set')
