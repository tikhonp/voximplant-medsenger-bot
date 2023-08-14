from datetime import time, datetime

from django.db import models
from django.db.models import Q

from forms.models import Call


class Contract(models.Model):
    contract_id = models.IntegerField(unique=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    agent_token = models.CharField(max_length=255)

    def __str__(self):
        return "Contract ({})".format(self.contract_id)

    @staticmethod
    def get_contracts_with_active_form(time_from: time, time_to: time, date_from: datetime):
        return (
            Contract
            .objects
            .select_related('forms')
            .exclude(forms__isnull=True)
            .filter(time_slot_set__time__in=(time_from, time_to))
            .exclude(
                Q(forms__call_set__updated_at__gte=date_from) &
                Q(forms__call_set__state=Call.State.SUCCESS)
            )
        )
