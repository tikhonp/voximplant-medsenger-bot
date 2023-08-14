from django.db import models

from medsenger_agent.models import Contract


class Form(models.Model):
    name = models.CharField(max_length=255)
    voximplant_id = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    contracts = models.ManyToManyField(Contract, related_name='forms')

    class Meta:
        ordering = ['name']

    def start_call(self, contract: Contract):
        print(f"Starting call for: {contract} with form: {self}")


class TimeSlot(models.Model):
    time = models.TimeField()

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='time_slot_set')

    class Meta:
        ordering = ['time']


class Call(models.Model):
    class State(models.TextChoices):
        SUCCESS = 'SUCCESS'

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='call_set')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='call_set')

    state = models.CharField(max_length=10, choices=State.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
