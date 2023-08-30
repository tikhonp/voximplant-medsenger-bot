from datetime import datetime, timedelta, time

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, QuerySet

from forms.models import Call, Form
from medsenger_agent.models import Contract


def get_contracts_with_active_form(time_from: time, time_to: time) -> QuerySet:
    return (
        Contract
        .objects
        .filter(is_active=True)
        .prefetch_related('forms')
        .prefetch_related('time_slot_set')
        .prefetch_related('forms__call_set')
        .exclude(forms__isnull=True)
        .filter(time_slot_set__time__range=(time_from, time_to))
    )


def check_current_calls():
    print("CALLED: check_current_calls")

    now = datetime.now()
    to_time = (now + timedelta(minutes=1)).time()
    from_time = now.time()
    from_date = now - timedelta(days=1)
    print(f"now: {now}\nto_time: {to_time}\nfrom_date: {from_date}")

    contracts_with_active_forms = get_contracts_with_active_form(from_time, to_time)
    print("contracts_with_active_forms: ", contracts_with_active_forms)

    for contract in contracts_with_active_forms:
        print("CONTRACT: ", contract)
        form = contract.forms.exclude(
            scenario_id__in=Call.objects.filter(
                updated_at__gte=from_date,
                state=Call.State.SUCCESS,
                contract=contract
            ).values('form')
        ).first()
        print("form: ", form)
        if form is not None:
            Call.start(contract, form)

    print("FINISHED")


def start_call(contract_id: int, form_id: int):
    try:
        contract = Contract.objects.get(contract_id=contract_id)
    except ObjectDoesNotExist:
        print(f"Failed to find contract with id: {contract_id}")
        return

    try:
        form = Form.objects.get(scenario_id=form_id)
    except ObjectDoesNotExist:
        print(f"Failed to find form with id: {form_id}")
        return

    call = Call.start(contract, form)
    print(f"Started: {call}")
