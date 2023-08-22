from django.contrib import admin

from forms import models


@admin.register(models.Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('name', 'scenario_id', 'is_active')


@admin.register(models.TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('time', 'contract')


@admin.register(models.Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('form', 'state', 'created_at', 'contract')
    readonly_fields = ('created_at', 'updated_at')
