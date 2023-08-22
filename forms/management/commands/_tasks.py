from datetime import datetime, timedelta, time

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, QuerySet

from forms.models import Call, Form
from medsenger_agent.models import Contract


def get_contracts_with_active_form(time_from: time, time_to: time, date_from: datetime) -> QuerySet:
    return (
        Contract
        .objects
        # .select_related('forms')
        .exclude(forms__isnull=True)
        .filter(time_slot_set__time__in=(time_from, time_to))
        .exclude(
            Q(forms__call_set__updated_at__gte=date_from) &
            Q(forms__call_set__state=Call.State.SUCCESS)
        )
    )


def check_current_calls():
    now = datetime.now()
    to_time = (now + timedelta(minutes=1)).time()
    from_date = now - timedelta(days=1)

    contracts_with_active_forms = get_contracts_with_active_form(now.time(), to_time, from_date)

    for contract in contracts_with_active_forms:
        forms = contract.forms.exclude(
            Q(forms__call_set__updated_at__gte=from_date) &
            Q(forms__call_set__state=Call.State.SUCCESS)
        )

        for form in forms:
            Call.start(contract, form)

    print("kek")


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
