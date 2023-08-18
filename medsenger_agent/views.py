from datetime import time

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.response import Response

from forms.models import Form, TimeSlot
from medsenger_agent import serializers
from medsenger_agent.models import Contract

MEDSENGER_APP_KEY = settings.MEDSENGER_APP_KEY
HOST = settings.HOST


class InitAPIView(CreateAPIView):
    serializer_class = serializers.ContractCreateSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return HttpResponse("ok")


class RemoveContractAPIView(GenericAPIView):
    serializer_class = serializers.ContractRemoveSerializer
    queryset = Contract.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = get_object_or_404(self.get_queryset(), contract_id=serializer.data['contract_id'])
        instance.is_active = False
        instance.save()

        return HttpResponse("ok")


class StatusAPIView(GenericAPIView):
    serializer_class = serializers.StatusSerializer
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


class SettingsFormsUpdate(GenericAPIView):
    serializer_class = serializers.SettingsFormSerializer
    queryset = Contract.objects.all()

    def process_request(self, request) -> (int, Contract):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = get_object_or_404(
            self.get_queryset(),
            agent_token=request.query_params.get('agent_token')
        )

        return serializer.data['form_id'], instance

    def post(self, request):
        form_id, contract = self.process_request(request)
        contract.forms.add(
            get_object_or_404(Form.objects.all(), id=form_id)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request):
        form_id, contract = self.process_request(request)
        contract.forms.remove(
            get_object_or_404(Form.objects.all(), id=form_id)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class SettingsTimeSlotsUpdate(GenericAPIView):
    serializer_class = serializers.SettingsTimeSlotSerializer
    queryset = Contract.objects.all()

    def process_request(self, request) -> (time, Contract):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = get_object_or_404(
            self.get_queryset(),
            agent_token=request.query_params.get('agent_token')
        )

        return serializer.data['time'], instance

    def post(self, request):
        time_data, contract = self.process_request(request)
        time_slot, _ = TimeSlot.objects.get_or_create(time=time_data, contract=contract)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request):
        time_data, contract = self.process_request(request)
        contract.time_slot_set.filter(time=time_data).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContractDetail(RetrieveAPIView):
    queryset = Contract.objects.all()
    serializer_class = serializers.ContractSerializer

    def get_object(self):
        return get_object_or_404(self.get_queryset(), agent_token=self.request.query_params.get('agent_token'))


@require_http_methods(['GET'])
def settings(request):
    if request.GET.get('api_key', '') != MEDSENGER_APP_KEY:
        return HttpResponse('"invalid key"', content_type='application/json', status=status.HTTP_401_UNAUTHORIZED)
    contract_id = request.GET.get('contract_id')
    contract = get_object_or_404(Contract.objects.all(), contract_id=contract_id)
    return render(request, 'settings.html', {
        'contract_id': contract_id,
        'base_url': HOST,
        'agent_token': contract.agent_token,
    })
