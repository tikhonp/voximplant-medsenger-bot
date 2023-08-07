from rest_framework.response import Response
from rest_framework.views import APIView

from forms.models import Form
from forms.serializers import FormSerializer


class FormList(APIView):
    """List of all forms for settings page."""

    def get(self, request):
        forms = Form.objects.filter(is_active=True)
        serializer = FormSerializer(forms, many=True)
        return Response(serializer.data)
