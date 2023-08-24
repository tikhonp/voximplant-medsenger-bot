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
