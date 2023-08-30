from __future__ import annotations

from django.conf import settings
from django.db import models
from django.db.models import Sum, Case, When

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

        @staticmethod
        def get_failure_states() -> [Call.State]:
            return [Call.State.FAILED_OUTBOUND_CALL, Call.State.VOICEMAIL_DETECTED]

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='call_set')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='call_set')

    state = models.CharField(max_length=22, choices=State.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_incoming = models.BooleanField(default=False)

    class Meta:
        ordering = ('-updated_at',)

    def __str__(self):
        return (f"Call(id={self.id}, form={self.form.scenario_id}, "
                f"contract={self.contract.contract_id}, state={self.state})")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.state in Call.State.get_failure_states():
            self.on_call_fail()

    def on_call_fail(self, n_max_failed_call: int = 3):
        """Check if n_max_failed_call of last calls to this contract failed. And send message to doctor about it."""

        calls = Call.objects.filter(contract=self.contract)

        last_success_calls_number = (calls[:n_max_failed_call].aggregate(
            success_calls=Sum(Case(When(state=Call.State.SUCCESS, then=1)), output_field=models.IntegerField())))

        if calls.count() >= n_max_failed_call and last_success_calls_number.get('success_calls') == 0:
            settings.MEDSENGER_API_CLIENT.send_message(self.contract.contract_id,
                                                       "Нам не удается дозвониться до пациента, пожалуйста, проверьте!",
                                                       only_doctor=True, is_urgent=True)

    def run_scenario(self):
        if not run_scenario(self.form.scenario_id, self.contract.patient_phone, self.id, self.contract.agent_token):
            self.state = Call.State.RUN_SCENARIO_FAILED
            self.save()

    def finish_form(self, form_params):
        self.state = Call.State.SUCCESS
        Form.commit_on_finish(self.contract, form_params)
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
