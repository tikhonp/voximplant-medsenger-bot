import csv

from django.contrib import admin
from django.http import HttpResponse

from forms import models


@admin.register(models.Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('name', 'scenario_id', 'is_active')


@admin.register(models.TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('time', 'connected_form')


@admin.action(description="Export selected calls as CSV")
def export_calls_as_csv(self, request, queryset):
    field_names = ['id', 'created_at', 'updated_at', 'state', 'patient_name', 'patient_phone', 'is_incoming']

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={"exported_voximplant_calls"}.csv'

    writer = csv.writer(response)
    writer.writerow(field_names)

    for obj in queryset:
        writer.writerow([
            obj.id, obj.created_at, obj.updated_at, obj.state,
            obj.connected_form.contract.patient_name,
            obj.connected_form.contract.patient_phone,
            obj.is_incoming
        ])

    return response


@admin.register(models.call.Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('id', 'connected_form', 'state', 'created_at')
    list_filter = ('created_at', 'state', 'is_incoming')
    readonly_fields = ('created_at', 'updated_at')
    actions = [export_calls_as_csv]


@admin.register(models.ConnectedForm)
class ConnectedFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract', 'form', 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('is_active',)
