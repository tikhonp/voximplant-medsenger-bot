from django.db import models

from forms.models.form import Form
from medsenger_agent.models import Contract
from utils.voximplant import run_scenario


class Call(models.Model):
    class State(models.TextChoices):
        PHONE_IS_NONE = 'PHONE_IS_NONE'
        CREATED = 'CREATED'
        SUCCESS = 'SUCCESS'
        RUN_SCENARIO_FAILED = 'RUN_SCENARIO_FAILED'

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='call_set')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='call_set')

    state = models.CharField(max_length=10, choices=State.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def run_scenario(self):
        if not run_scenario(
                self.form.voximplant_scenario_id,
                self.contract.phone,
                self.id,
                self.contract.agent_token):
            self.state = Call.State.RUN_SCENARIO_FAILED
            self.save()
