from rest_framework import serializers

from forms.models import Form, TimeSlot, Call


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ['id', 'name']


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'time']


class UpdateCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = ['id', 'state']
