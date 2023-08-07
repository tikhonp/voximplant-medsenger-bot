from django.db import models


class Contract(models.Model):
    contract_id = models.IntegerField(unique=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    agent_token = models.CharField(max_length=255)

    def __str__(self):
        return "Contract ({})".format(self.contract_id)
