from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, GenericAPIView, ListCreateAPIView, RetrieveDestroyAPIView, \
    RetrieveAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from forms.models import Form, TimeSlot, Call
from forms.serializers import TimeSlotSerializer, FormSerializer, CallSerializer
from medsenger_agent.models import Contract
from medsenger_agent.serializers import ContractSerializer, ApiKeyBodySerializer, OrderSerializer
from utils.contract_by_agent_token_mixin import ContractByAgentTokenMixin
from utils.drf_permissions.api_key_permission import ApiKeyPermission


class MedsengerAgentInitView(CreateAPIView):
    serializer_class = ContractSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return HttpResponse("ok")


class MedsengerAgentRemoveContractView(GenericAPIView):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = get_object_or_404(self.get_queryset(), contract_id=serializer.data.get('contract_id'))
        instance.is_active = False
        instance.save()

        return HttpResponse("ok")


class MedsengerAgentStatusView(GenericAPIView):
    serializer_class = ApiKeyBodySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tracked_contracts = Contract.objects.filter(is_active=True).values('contract_id')
        tracked_contract_ids = [i.get('contract_id') for i in tracked_contracts]

        data = {
            'is_tracking_data': True,
            'supported_scenarios': [],
            'tracked_contracts': tracked_contract_ids
        }
        return Response(data)


# noinspection PyMethodMayBeStatic
class MedsengerAgentSettingsView(APIView):
    """
    Medsenger agent /settings page.

    Requires `api_key` and `contract_id` query params.
    """

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'settings.html'
    permission_classes = [ApiKeyPermission]
    authentication_classes = []

    def get(self, request):
        contract_id = request.GET.get('contract_id')
        contract = get_object_or_404(Contract.objects.all(), contract_id=contract_id)
        return Response({'contract_id': contract_id, 'base_url': settings.HOST, 'agent_token': contract.agent_token})


class MedsengerAgentOrderView(GenericAPIView):
    """
    Medsenger order
    """

    serializer_class = OrderSerializer
    queryset = Contract.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = get_object_or_404(self.get_queryset(), contract_id=serializer.data.get('contract_id'))
        instance.update_user()
        return HttpResponse("ok")


class ContractFormsView(ListCreateAPIView, ContractByAgentTokenMixin):
    """
    Get list of forms for contract or add new form to contract.

    Note: that `agent_token` must be provided
    """

    serializer_class = FormSerializer

    def get_queryset(self):
        return Form.objects.filter(contracts=self.get_contract())

    def perform_create(self, serializer):
        self.get_contract().forms.add(
            get_object_or_404(Form.objects.all(), scenario_id=serializer.data.get('scenario_id')))


class ContractFormDetailView(RetrieveDestroyAPIView, ContractByAgentTokenMixin):
    """
    Get form by id or delete relation from contract.

    Note: that `agent_token` must be provided
    """

    serializer_class = FormSerializer

    def get_queryset(self):
        return Form.objects.filter(contracts=self.get_contract())

    def perform_destroy(self, instance):
        instance.contracts.remove(self.get_contract())


class ContractTimeSlotsView(ListCreateAPIView, ContractByAgentTokenMixin):
    """
    Get list of contract related time slots or add time slot to contract.

    Note: that `agent_token` must be provided
    """

    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        return TimeSlot.objects.filter(contract=self.get_contract())

    def perform_create(self, serializer):
        TimeSlot.objects.get_or_create(time=serializer.data['time'], contract=self.get_contract())


class ContractTimeSlotDetailView(RetrieveDestroyAPIView, ContractByAgentTokenMixin):
    """
    Get time slot by id or delete it.

    Note: that `agent_token` must be provided
    """

    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        return TimeSlot.objects.filter(contract=self.get_contract())


class ContractCallsView(ListCreateAPIView, ContractByAgentTokenMixin):
    """
    Get list of call related to contract

    Note: that `agent_token` must be provided
    """

    serializer_class = CallSerializer

    def get_queryset(self):
        return Call.objects.filter(contract=self.get_contract()).select_related('form')

    def perform_create(self, serializer):
        serializer.save(contract=self.get_contract())


class ContractView(RetrieveAPIView, ContractByAgentTokenMixin):
    """
    Get contract data by agent token

    Note: that `agent_token` must be provided
    """

    serializer_class = ContractSerializer

    def get_object(self):
        return self.get_contract()
