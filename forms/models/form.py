from django.db import models

from medsenger_agent.models import Contract


class Form(models.Model):
    name = models.CharField(max_length=255)
    voximplant_scenario_id = models.IntegerField()
    is_active = models.BooleanField(default=True)

    contracts = models.ManyToManyField(Contract, related_name='forms')

    class Meta:
        ordering = ['name']
