from rest_framework import serializers

from forms.models import Form, TimeSlot, Call, ConnectedForm


class FormSerializer(serializers.ModelSerializer):
    scenario_id = serializers.IntegerField()

    class Meta:
        model = Form
        fields = ('scenario_id', 'name')
        extra_kwargs = {'scenario_id': {'required': True},
                        'name': {'required': False, 'allow_blank': True}}


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'


# noinspection PyMethodMayBeStatic
class CallSerializer(serializers.ModelSerializer):
    state_ru_localized = serializers.SerializerMethodField()

    class Meta:
        model = Call
        fields = ('id', 'state', 'created_at', 'connected_form',
                  'updated_at', 'is_incoming', 'state_ru_localized')

    def to_representation(self, instance):
        representation = super(CallSerializer, self).to_representation(instance)
        representation['form'] = FormSerializer(instance.connected_form.form).data
        return representation

    def get_state_ru_localized(self, obj):
        return Call.State(obj.state).ru_localized


class UpdateCallSerializer(serializers.Serializer):
    voximplant_state = serializers.ChoiceField(choices=Call.VoximplantState.choices)
    scenario_state = serializers.ChoiceField(choices=Call.State.choices)


class FormValueSerializer(serializers.Serializer):
    category_name = serializers.CharField()
    value = serializers.CharField()


class ConnectedFormSerializer(serializers.ModelSerializer):
    time_slot_set = TimeSlotSerializer(many=True, read_only=True)

    class Meta:
        model = ConnectedForm
        exclude = ('contract',)

    def to_representation(self, instance):
        representation = super(ConnectedFormSerializer, self).to_representation(instance)
        representation['form'] = FormSerializer(instance.form).data
        return representation
