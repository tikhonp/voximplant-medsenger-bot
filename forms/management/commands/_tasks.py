from datetime import datetime, timedelta, time

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from forms.models import Call, Form
from medsenger_agent.models import Contract


def get_contracts_with_active_form(time_from: time, time_to: time) -> QuerySet:
    """
    Check if there are any active contracts with forms and time slots in given time range.
    """

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
    """
    Check for available time_slots in current time and find contracts where call must execute and run calls.
    Time interval is now plus one minute.
    """

    now = datetime.now()
    from_time = now.time()
    to_time = (now + timedelta(minutes=1)).time()
    print(f"\nnow: {now}\nto_time: {to_time}")

    contracts_with_active_forms = get_contracts_with_active_form(from_time, to_time)
    print("contracts_with_active_forms: ", contracts_with_active_forms)

    for contract in contracts_with_active_forms:
        print("CONTRACT: ", contract)

        current_day_start_date = datetime.combine(now.date(), time(0, 0, 0))
        if contract.timezone_offset is not None:
            current_day_start_date = current_day_start_date - timedelta(minutes=contract.timezone_offset)

        form = contract.forms.exclude(
            scenario_id__in=Call.objects.filter(
                updated_at__gte=current_day_start_date,
                state=Call.State.SUCCESS,
                contract=contract
            ).values('form')
        ).first()  # execute only one form at time slot
        print("form: ", form)
        if form is not None:
            Call.start(contract, form)


def start_call(contract_id: int, form_id: int):
    """
    Manually start a call, with contract_id and form_id.
    """

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
