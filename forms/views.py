from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import ListAPIView

from forms.models import Form
from forms.serializers import FormSerializer


class FormList(ListAPIView):
    """List of all forms for settings page."""

    queryset = Form.objects.filter(is_active=True)
    serializer_class = FormSerializer


@csrf_exempt
def call(request):
    print(request.body)
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)
