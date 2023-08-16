from django.conf import settings
from django.db import models
from medsenger_api import AgentApiClient

MEDSENGER_API_CLIENT: AgentApiClient = settings.MEDSENGER_API_CLIENT


class Contract(models.Model):
    contract_id = models.IntegerField(unique=True, primary_key=True)
    phone = models.CharField(max_length=11, null=True, default=None)
    is_active = models.BooleanField(default=True)
    agent_token = models.CharField(max_length=255)

    def __str__(self):
        return "Contract ({})".format(self.contract_id)

    def save(self, *args, **kwargs):
        metadata = MEDSENGER_API_CLIENT.get_patient_info(self.contract_id)
        self.phone = metadata.get('phone')
        super().save(*args, **kwargs)
