from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from forms.models import Form, Call, TimeSlot
from forms.serializers import FormSerializer, UpdateCallSerializer
from medsenger_agent.models import Contract
from utils.agent_token_permission import AgentTokenPermission


class FormList(ListAPIView):
    """List of all forms for settings page."""

    queryset = Form.objects.filter(is_active=True)
    serializer_class = FormSerializer
    permission_classes = [AgentTokenPermission]
    authentication_classes = []


class UpdateCall(UpdateAPIView):
    """Update call from voximplant scenario."""

    queryset = Call.objects.all()
    serializer_class = UpdateCallSerializer
    permission_classes = [AgentTokenPermission]
    authentication_classes = []


class GetNextTimeSlot(APIView):
    """
    Get next available time slot for contract and get time 'HH:MM:SS' and is_tomorrow flag.
    Note: that `agent_token` must be provided
    """

    def get(self, request):
        contract = get_object_or_404(
            Contract.objects.all(),
            agent_token=request.query_params.get('agent_token')
        )
        time, is_tomorrow = TimeSlot.get_next_timeslot(datetime.now(), contract=contract)
        return Response({
            'time': time,
            'is_tomorrow': is_tomorrow
        })
