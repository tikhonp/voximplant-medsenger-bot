from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, GenericAPIView, ListCreateAPIView, \
    RetrieveDestroyAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from forms.models import Form, TimeSlot
from forms.serializers import TimeSlotSerializer, FormSerializer
from medsenger_agent import serializers
from medsenger_agent.models import Contract
from utils.api_key_permission import ApiKeyPermission


class MedsengerAgentInitView(CreateAPIView):
    serializer_class = serializers.ContractCreateSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return HttpResponse("ok")


class MedsengerAgentRemoveContractView(GenericAPIView):
    serializer_class = serializers.ContractRemoveSerializer
    queryset = Contract.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = get_object_or_404(self.get_queryset(), contract_id=serializer.data['contract_id'])
        instance.is_active = False
        instance.save()

        return HttpResponse("ok")


class MedsengerAgentStatusView(GenericAPIView):
    serializer_class = serializers.ApiKeyBodySerializer
    queryset = Contract.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'is_tracking_data': True,
            'supported_scenarios': [],
            'tracked_contracts': [i.contract_id for i in self.get_queryset().filter(is_active=True)]
        }
        return Response(data)


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
        return Response({
            'contract_id': contract_id,
            'base_url': settings.HOST,
            'agent_token': contract.agent_token,
        })


class ContractFormsView(ListCreateAPIView):
    """
    Get list of forms for contract or add new form to contract.

    Note: that `agent_token` must be provided
    """

    serializer_class = FormSerializer

    def get_queryset(self):
        contract = get_object_or_404(
            Contract.objects.all(),
            agent_token=self.request.query_params.get('agent_token')
        )
        return Form.objects.filter(contracts=contract)

    def perform_create(self, serializer):
        contract = get_object_or_404(
            Contract.objects.all(),
            agent_token=self.request.query_params.get('agent_token')
        )
        contract.forms.add(
            get_object_or_404(Form.objects.all(), scenario_id=serializer.data.get('scenario_id'))
        )


class ContractFormDetailView(RetrieveDestroyAPIView):
    """
    Get form by id or delete relation from contract.

    Note: that `agent_token` must be provided
    """

    serializer_class = FormSerializer

    def get_queryset(self):
        return Form.objects.filter(
            contracts=get_object_or_404(
                Contract.objects.all(),
                agent_token=self.request.query_params.get('agent_token')
            )
        )

    def perform_destroy(self, instance):
        instance.contracts.remove(
            get_object_or_404(
                Contract.objects.all(),
                agent_token=self.request.query_params.get('agent_token')
            )
        )


class ContractTimeSlotsView(ListCreateAPIView):
    """
    Get list of contract related time slots or add time slot to contract.

    Note: that `agent_token` must be provided
    """

    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        contract = get_object_or_404(
            Contract.objects.all(),
            agent_token=self.request.query_params.get('agent_token')
        )
        return TimeSlot.objects.filter(contract=contract)

    def perform_create(self, serializer):
        contract = get_object_or_404(
            Contract.objects.all(),
            agent_token=self.request.query_params.get('agent_token')
        )
        TimeSlot.objects.get_or_create(time=serializer.data['time'], contract=contract)


class ContractTimeSlotDetailView(RetrieveDestroyAPIView):
    """
    Get time slot by id or delete it.

    Note: that `agent_token` must be provided
    """

    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        contract = get_object_or_404(
            Contract.objects.all(),
            agent_token=self.request.query_params.get('agent_token')
        )
        return TimeSlot.objects.filter(contract=contract)
