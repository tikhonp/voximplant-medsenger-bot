from random import choice

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from forms.models import Call
from forms_ai.serializers import CallRequestSerializer
from utils.drf_permissions.agent_token_permission import AgentTokenPermission


class CallRequest(GenericAPIView):
    """
    Test for more powerful voice dialog engine

    Note: that `agent_token` must be provided.
    """

    queryset = Call.objects.all()
    serializer_class = CallRequestSerializer
    permission_classes = [AgentTokenPermission]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(f"Call <{instance.id}> got text: {serializer.data.get('field')}")
        if 'нет' in serializer.data.get('field'):
            return Response({
                'action': CallRequestSerializer.Action.FINISH_CALL,
                'field': '',
            })
        else:
            return Response({
                'action': CallRequestSerializer.Action.TEXT,
                'field': choice(['лол', 'кек', 'ляля']),
            })
