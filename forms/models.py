from django.db import models

from medsenger_agent.models import Contract


class Form(models.Model):
    name = models.CharField(max_length=255)
    voximplant_id = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    contracts = models.ManyToManyField(Contract)

    class Meta:
        ordering = ['name']


class TimeSlot(models.Model):
    time = models.TimeField()

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='time_slot_set')

    class Meta:
        ordering = ['time']
