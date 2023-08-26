from rest_framework import serializers

from forms.models import Form, TimeSlot, Call


class FormSerializer(serializers.ModelSerializer):
    scenario_id = serializers.IntegerField()

    class Meta:
        model = Form
        fields = ('scenario_id', 'name')
        extra_kwargs = {'scenario_id': {'required': True}, 'name': {'required': False, 'allow_blank': True}}


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ('id', 'time')


class CallSerializer(serializers.ModelSerializer):
    form = FormSerializer(read_only=True)

    class Meta:
        model = Call
        fields = ('id', 'state', 'created_at', 'updated_at', 'form')


class FormValueSerializer(serializers.Serializer):
    category_name = serializers.CharField()
    value = serializers.CharField()
