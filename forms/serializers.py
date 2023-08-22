from rest_framework import serializers

from forms.models import Form, TimeSlot, Call


class FormSerializer(serializers.ModelSerializer):
    scenario_id = serializers.IntegerField()

    class Meta:
        model = Form
        fields = ['scenario_id', 'name']
        extra_kwargs = {
            'scenario_id': {'required': True},
            'name': {'required': False, 'allow_blank': True}
        }


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'time']


class UpdateCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = ['id', 'state']
