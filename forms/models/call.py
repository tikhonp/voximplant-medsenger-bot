from __future__ import annotations

from typing import Dict

from django.conf import settings
from django.db import models
from django.db.models import Sum, Case, When

from forms.models.form import Form
from medsenger_agent.models import Contract
from utils.voximplant import run_scenario


class Call(models.Model):
    """All information about single call, updates by voximplant during call."""

    class VoximplantState(models.IntegerChoices):
        """https://voximplant.com/kit/docs/editor/standardvariables#call-object"""

        VOICEMAIL_DETECTOR = 1
        INITIATED_BY_THE_CALLEE = 2
        END_OF_THE_SCENARIO = 3
        THE_CALL_WAS_ACCEPTED = 200
        THE_NUMBER_IS_BUSY = 486
        THE_CALLEE_HAS_NOT_ANSWERED_408 = 408
        THE_CALLEE_HAS_NOT_ANSWERED_487 = 487
        THE_CALLEE_HAS_NOT_ANSWERED_500 = 500
        THE_CALL_HAS_BEEN_DECLINED = 603
        INVALID_NUMBER = 404
        THE_CALLEE_IS_UNAVAILABLE = 480
        CALL_IS_FORBIDDEN = 403
        THE_WAS_NO_CALL = 0
        THE_CALL_WAS_INTERRUPTED_BY_THE_STOP_BUTTON = 4

    class State(models.TextChoices):
        CREATED = 'CREATED'
        SUCCESS = 'SUCCESS'
        VOICEMAIL_DETECTED = 'VOICEMAIL_DETECTED'
        THE_NUMBER_IS_BUSY = 'THE_NUMBER_IS_BUSY'
        THE_CALLEE_HAS_NOT_ANSWERED = 'THE_CALLEE_HAS_NOT_ANSWERED'
        THE_CALLEE_HAS_BEEN_DECLINED = 'THE_CALLEE_HAS_BEEN_DECLINED'
        THE_CALLEE_STOPPED_CALL = 'THE_CALLEE_STOPPED_CALL'
        INVALID_NUMBER = 'INVALID_NUMBER'
        THE_CALLEE_IS_UNAVAILABLE = 'THE_CALLEE_IS_UNAVAILABLE'
        CALL_IS_FORBIDDEN = 'CALL_IS_FORBIDDEN'
        PHONE_IS_NONE = 'PHONE_IS_NONE'
        RUN_SCENARIO_FAILED = 'RUN_SCENARIO_FAILED'
        DENIED_BY_USER = 'DENIED_BY_USER'
        FAILED_DURING_SCENARIO = 'FAILED_DURING_SCENARIO'

        @staticmethod
        def get_failure_states() -> [Call.State]:
            return [Call.State.VOICEMAIL_DETECTED, Call.State.THE_NUMBER_IS_BUSY,
                    Call.State.THE_CALLEE_HAS_NOT_ANSWERED, Call.State.THE_CALLEE_HAS_BEEN_DECLINED,
                    Call.State.INVALID_NUMBER, Call.State.THE_CALLEE_IS_UNAVAILABLE, Call.State.CALL_IS_FORBIDDEN,
                    Call.State.PHONE_IS_NONE, Call.State.RUN_SCENARIO_FAILED, Call.State.DENIED_BY_USER,
                    Call.State.DENIED_BY_USER, Call.State.FAILED_DURING_SCENARIO]

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='call_set')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='call_set')

    state = models.CharField(max_length=28, choices=State.choices)

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

    def update_state_from_scenario(self, scenario_state: Call.State, voximplant_state: Call.VoximplantState):
        """
        Compile two statuses from voximplant and call into single db status.
        """

        states_dict = {
            Call.VoximplantState.VOICEMAIL_DETECTOR: Call.State.VOICEMAIL_DETECTED,
            Call.VoximplantState.INITIATED_BY_THE_CALLEE: Call.State.THE_CALLEE_STOPPED_CALL,
            Call.VoximplantState.THE_NUMBER_IS_BUSY: Call.State.THE_NUMBER_IS_BUSY,
            Call.VoximplantState.THE_CALLEE_HAS_NOT_ANSWERED_487: Call.State.THE_CALLEE_HAS_NOT_ANSWERED,
            Call.VoximplantState.THE_CALLEE_HAS_NOT_ANSWERED_408: Call.State.THE_CALLEE_HAS_NOT_ANSWERED,
            Call.VoximplantState.THE_CALLEE_HAS_NOT_ANSWERED_500: Call.State.THE_CALLEE_HAS_NOT_ANSWERED,
            Call.VoximplantState.THE_CALL_HAS_BEEN_DECLINED: Call.State.THE_CALLEE_HAS_BEEN_DECLINED,
            Call.VoximplantState.INVALID_NUMBER: Call.State.INVALID_NUMBER,
            Call.VoximplantState.THE_CALLEE_IS_UNAVAILABLE: Call.State.THE_CALLEE_IS_UNAVAILABLE,
            Call.VoximplantState.CALL_IS_FORBIDDEN: Call.State.CALL_IS_FORBIDDEN,
        }
        self.state = states_dict.get(voximplant_state, scenario_state)
        self.save()

    def on_call_fail(self, n_max_failed_call: int = 3):
        """
        Check if n_max_failed_call of last calls to this contract failed. And send message to doctor about it.
        """

        calls = Call.objects.filter(contract=self.contract)

        last_success_calls_number = (calls[:n_max_failed_call].aggregate(
            success_calls=Sum(Case(When(state=Call.State.SUCCESS, then=1)), output_field=models.IntegerField())))

        if calls.count() >= n_max_failed_call and last_success_calls_number.get('success_calls') == 0:
            settings.MEDSENGER_API_CLIENT.send_message(self.contract.contract_id,
                                                       "Нам не удается дозвониться до пациента, пожалуйста, проверьте!",
                                                       only_doctor=True, is_urgent=True)

    def run_scenario(self):
        """
        Run a voximplant scenario (execute call).
        """

        if not run_scenario(self.form.scenario_id, self.contract.patient_phone.as_e164,
                            self.id, self.contract.agent_token):
            self.state = Call.State.RUN_SCENARIO_FAILED
            self.save()

    def finish_call(self, form_params: Dict[str, str]):
        """
        Commit records to form and finish call.
        """

        self.state = Call.State.SUCCESS
        Form.commit_on_finish(self.contract, form_params)
        self.save()

    @staticmethod
    def start(contract: Contract, form: Form) -> Call:
        """
        Start call for specific contract and form.
        Creates `Call` object checks contract for phone is not None and runs call.
        """

        if contract.patient_phone is None:
            call = Call(form=form, contract=contract, state=Call.State.PHONE_IS_NONE)
            call.save()
            return call

        call = Call(form=form, contract=contract, state=Call.State.CREATED)
        call.save()
        call.run_scenario()
        return call
