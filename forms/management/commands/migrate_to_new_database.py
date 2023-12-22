import json

from django.core.management.base import BaseCommand

from forms.models import Form, ConnectedForm, TimeSlot, Call
from medsenger_agent.models import Contract


def fill_time_slots_for_connected_form(data, connected_form, contract_id):
    time_slots = filter(
        lambda x: x.get('model') == 'forms.timeslot' and x.get('fields').get('contract') == contract_id, data)

    for time_slot in time_slots:
        TimeSlot(
            time=time_slot.get('fields').get('time'),
            connected_form=connected_form
        ).save()


def fill_base_forms(data):
    forms = filter(lambda x: x.get('model') == 'forms.form', data)

    for form in forms:
        form_model = Form(
            pk=form.get('pk'),
            name=form.get('fields').get('name'),
            is_active=form.get('fields').get('is_active'),
        )
        form_model.save()

        for contract_id in form.get('fields').get('contracts'):
            contract = Contract.objects.get(contract_id=contract_id)
            connected_form = ConnectedForm(
                contract=contract,
                form=form_model,
            )
            connected_form.save()
            fill_time_slots_for_connected_form(data, connected_form, contract_id)


def fill_contracts(data):
    contracts = filter(lambda x: x.get('model') == 'medsenger_agent.contract', data)

    for contract in contracts:
        Contract(
            pk=contract.get('pk'),
            is_active=contract.get('fields').get('is_active'),
            agent_token=contract.get('fields').get('agent_token'),
            patient_name=contract.get('fields').get('patient_name'),
            patient_sex=contract.get('fields').get('patient_sex'),
            patient_phone=contract.get('fields').get('patient_phone'),
            timezone_offset=contract.get('fields').get('timezone_offset'),
        ).save()


def fill_calls(data):
    calls = filter(lambda x: x.get('model') == 'forms.call', data)

    for call in calls:
        contract = Contract.objects.get(contract_id=call.get('fields').get('contract'))
        form = Form.objects.get(pk=call.get('fields').get('form'))

        try:
            connected_form = contract.connected_forms.get(form=form)
        except ConnectedForm.DoesNotExist:
            continue

        Call(
            connected_form=connected_form,
            state=call.get('fields').get('state'),
            created_at=call.get('fields').get('created_at'),
            updated_at=call.get('fields').get('updated_at'),
            is_incoming=call.get('fields').get('is_incoming'),
        ).save()


class Command(BaseCommand):
    help = 'Start worker for executing calls at specific time.'

    def add_arguments(self, parser):
        parser.add_argument("--json_file", required=True, type=str)

    def handle(self, *args, **options):
        with open(options.get('json_file')) as f:
            data = json.load(f)

        fill_contracts(data)
        fill_base_forms(data)
        fill_calls(data)