from django.conf import settings
from django.db import models


class Contract(models.Model):
    contract_id = models.IntegerField(unique=True, primary_key=True)

    is_active = models.BooleanField(default=True)
    agent_token = models.CharField(max_length=255)

    patient_name = models.CharField(max_length=255)
    patient_email = models.EmailField(null=True, default=None)
    patient_sex = models.CharField(max_length=20)
    patient_phone = models.CharField(max_length=11, null=True, default=None)

    def __str__(self):
        return "Contract ({})".format(self.contract_id)

    def save(self, *args, **kwargs):
        metadata = settings.MEDSENGER_API_CLIENT.get_patient_info(self.contract_id)
        self.patient_name = metadata.get('name', '')
        self.patient_email = metadata.get('email')
        self.patient_sex = metadata.get('sex')
        self.phone = metadata.get('phone')
        agent_token = settings.MEDSENGER_API_CLIENT.get_agent_token(self.contract_id)
        self.agent_token = agent_token.get('agent_token', '')
        super().save(*args, **kwargs)
