from django.db import models

from forms.models import Form
from medsenger_agent.models import Contract


class ConnectedForm(models.Model):
    """Contains connection between contract and connected form and attached timeslots for this connection."""

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='connected_forms')
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='connected_forms')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
