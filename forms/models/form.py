from django.conf import settings
from django.db import models

from medsenger_agent.models import Contract


class Form(models.Model):
    """Voximplant scenario model, related by `scenario_id` which is equal to voximplant scenario ID."""

    scenario_id = models.IntegerField(primary_key=True)

    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    contracts = models.ManyToManyField(Contract, related_name='forms', blank=True)

    class Meta:
        ordering = ('name',)

    @staticmethod
    def commit_on_finish(contract: Contract, form_params: dict[str, str]):
        """
        Commit records (`form_params`) to Medsenger using add_records.
        """

        settings.MEDSENGER_API_CLIENT.add_records(contract.contract_id, form_params)
