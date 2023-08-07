from django.contrib import admin

from medsenger_agent import models


@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_id', 'is_active')
