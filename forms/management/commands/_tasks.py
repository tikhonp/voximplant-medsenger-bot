from datetime import datetime, timedelta

from forms.models import Call
from medsenger_agent.models import Contract

from django.db.models import Q


def check_current_calls():
    now = datetime.now()
    to_time = (now + timedelta(minutes=1)).time()
    from_date = now - timedelta(days=1)

    contracts_with_active_forms = Contract.get_contracts_with_active_form(now.time(), to_time, from_date)

    for contract in contracts_with_active_forms:
        forms = contract.forms.exclude(
            Q(forms__call_set__updated_at__gte=from_date) &
            Q(forms__call_set__state=Call.State.SUCCESS)
        )

        for form in forms:
            form.start_call(contract)
