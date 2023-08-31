from datetime import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from forms.models import Form, Call, TimeSlot
from forms.serializers import FormSerializer, FormValueSerializer, UpdateCallSerializer
from medsenger_agent.models import Contract
from utils.contract_by_agent_token_mixin import ContractByAgentTokenMixin
from utils.drf_permissions.agent_token_permission import AgentTokenPermission


class FormList(ListAPIView):
    """
    List of all forms for settings page.

    Note: that `agent_token` must be provided.
    """

    queryset = Form.objects.filter(is_active=True)
    serializer_class = FormSerializer
    permission_classes = [AgentTokenPermission]
    authentication_classes = []


class RetrieveUpdateCall(GenericAPIView):
    """
    Update call from voximplant scenario.

    Note: that `agent_token` must be provided.
    """

    queryset = Call.objects.all()
    serializer_class = UpdateCallSerializer
    permission_classes = [AgentTokenPermission]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.update_state_from_scenario(**serializer.data)
        return Response(serializer.data)


class FinishScenario(GenericAPIView):
    """
    Finish scenario and commit final form data.

    Note: that `agent_token` must be provided.
    """

    queryset = Call.objects.all()
    serializer_class = FormValueSerializer
    permission_classes = [AgentTokenPermission]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        instance.finish_call(serializer.data)
        return Response(serializer.data)


class GetNextTimeSlot(APIView, ContractByAgentTokenMixin):
    """
    Get next available time slot for contract and get time (`HH:MM:SS`) and `is_tomorrow` flag.

    Note: that `agent_token` must be provided.
    """

    def get(self, request, *args, **kwargs):
        time, is_tomorrow = TimeSlot.get_next_timeslot(datetime.now(), contract=self.get_contract())
        return Response({'time': time, 'is_tomorrow': is_tomorrow})


# noinspection PyMethodMayBeStatic
class GetAgentToken(APIView):
    """
    Get agent token by phone number allow requests only from voximplant.
    Accepts `phone` and `voximplant_key` query params.
    """

    def get(self, request, *args, **kwargs):
        phone = request.query_params.get('phone')
        voximplant_key = request.query_params.get('voximplant_key')

        if phone is None or voximplant_key is None:
            raise ParseError("`phone` and `voximplant_key` are required query params")

        if settings.VOXIMPLANT_INBOUND_CALLS_SECRET_KEY != voximplant_key:
            raise PermissionDenied("`voximplant_key` is invalid.")

        contract = get_object_or_404(Contract.objects.all(), patient_phone=PhoneNumber.from_string(phone, region='RU'))

        return Response({'agent_token': contract.agent_token})
