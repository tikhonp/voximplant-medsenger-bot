from django.db import models

from medsenger_agent.models import Contract


class TimeSlot(models.Model):
    time = models.TimeField()

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='time_slot_set')

    class Meta:
        ordering = ['time']
