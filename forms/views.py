from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView

from forms.models import Form, Call
from forms.serializers import FormSerializer, UpdateCallSerializer
from utils.agent_token_permission import AgentTokenPermission


class FormList(ListAPIView):
    """List of all forms for settings page."""

    queryset = Form.objects.filter(is_active=True)
    serializer_class = FormSerializer
    permission_classes = [AgentTokenPermission]
    authentication_classes = []


class UpdateCall(UpdateAPIView):
    serializer_class = UpdateCallSerializer
    queryset = Call.objects.all()
    permission_classes = [AgentTokenPermission]
    authentication_classes = []


@csrf_exempt
def call(request):
    print(request.body)
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)
