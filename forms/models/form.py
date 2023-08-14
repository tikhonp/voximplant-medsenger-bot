from django.db import models

from forms.models import Call
from medsenger_agent.models import Contract


class Form(models.Model):
    name = models.CharField(max_length=255)
    voximplant_scenario_id = models.IntegerField()
    is_active = models.BooleanField(default=True)

    contracts = models.ManyToManyField(Contract, related_name='forms')

    class Meta:
        ordering = ['name']

    def start_call(self, contract: Contract) -> Call:
        if contract.phone is None:
            call = Call(form=self, contract=contract, state=Call.State.PHONE_IS_NONE)
            call.save()
            return call

        call = Call(form=self, contract=contract, state=Call.State.CREATED)
        call.save()
        call.run_scenario()
        return call
