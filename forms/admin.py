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
    list_display = ('id', 'form', 'state', 'created_at', 'contract')
    list_filter = ('state',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('form__id', 'contract__id')
    search_help_text = "Search by related 'form__id' or 'contract__id'."
