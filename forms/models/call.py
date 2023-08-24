from __future__ import annotations

from django.db import models

from forms.models.form import Form
from medsenger_agent.models import Contract
from utils.voximplant import run_scenario


class Call(models.Model):
    """All information about single call, updates by voximplant during call."""

    class State(models.TextChoices):
        PHONE_IS_NONE = 'PHONE_IS_NONE'
        CREATED = 'CREATED'
        SUCCESS = 'SUCCESS'
        RUN_SCENARIO_FAILED = 'RUN_SCENARIO_FAILED'
        FAILED_OUTBOUND_CALL = 'FAILED_OUTBOUND_CALL'
        VOICEMAIL_DETECTED = 'VOICEMAIL_DETECTED'
        DENIED_BY_USER = 'DENIED_BY_USER'
        FAILED_DURING_SCENARIO = 'FAILED_DURING_SCENARIO'

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='call_set')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='call_set')

    state = models.CharField(max_length=22, choices=State.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated_at',)

    def __str__(self):
        return (f"Call(id={self.id}, form={self.form.scenario_id}, "
                f"contract={self.contract.contract_id}, state={self.state})")

    def run_scenario(self):
        if not run_scenario(self.form.scenario_id, self.contract.patient_phone, self.id, self.contract.agent_token):
            self.state = Call.State.RUN_SCENARIO_FAILED
            self.save()

    @staticmethod
    def start(contract: Contract, form: Form) -> Call:
        if contract.patient_phone is None:
            call = Call(form=form, contract=contract, state=Call.State.PHONE_IS_NONE)
            call.save()
            return call

        call = Call(form=form, contract=contract, state=Call.State.CREATED)
        call.save()
        call.run_scenario()
        return call
