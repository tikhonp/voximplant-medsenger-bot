from datetime import datetime, timedelta, time

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet, Q

from forms.models import Call, ConnectedForm
from medsenger_agent.models import Contract


def get_contracts_with_active_form(time_from: time, time_to: time) -> QuerySet:
    """
    Check if there are any active contracts with forms and time slots in given time range.
    """

    return (
        Contract
        .objects
        .filter(is_active=True)
        .exclude(connected_forms__isnull=True)
        .filter(connected_forms__is_active=True)
        .filter(connected_forms__time_slot_set__time__range=(time_from, time_to))
        .prefetch_related('connected_forms')
        .prefetch_related('connected_forms__time_slot_set')
        .prefetch_related('connected_forms__call_set')
    )


def check_current_calls():
    """
    Check for available time_slots in current time and find contracts where call must execute and run calls.
    Time interval is now plus one minute.
    """

    now = datetime.now()
    print(f"\nnow: {now}")

    contracts_with_active_forms = get_contracts_with_active_form(
        time_from=now.time(),
        time_to=(now + timedelta(minutes=1)).time()
    )
    print("contracts_with_active_forms: ", contracts_with_active_forms)

    for contract in contracts_with_active_forms:
        print("CONTRACT: ", contract)

        current_day_start_date = datetime.combine(now.date(), time(0, 0, 0))
        if contract.timezone_offset is not None:
            current_day_start_date = current_day_start_date - timedelta(minutes=contract.timezone_offset)

        form = contract.connected_forms.exclude(
            pk__in=Call.objects.filter(
                Q(connected_form__contract=contract),

                # Exclude forms with success calls today
                Q(updated_at__gte=current_day_start_date, state=Call.State.SUCCESS) |

                # Exclude forms with recently started calls
                Q(created_at__gte=(now - timedelta(minutes=5)), state=Call.State.CREATED)
            ).values('connected_form')
        ).first()  # execute only one form at time slot
        print("form: ", form)
        if form is not None:
            Call.start(form)


def start_call(connected_form_id: int):
    """
    Manually start a call, with contract_id and connected_form_id.
    """

    try:
        form = ConnectedForm.objects.get(pk=connected_form_id)
    except ObjectDoesNotExist:
        print(f"Failed to find connected form with id: {connected_form_id}")
        return

    call = Call.start(form)
    print(f"Started: {call}")
