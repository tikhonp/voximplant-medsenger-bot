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


@admin.action(description="Export selected calls for statistic")
def export_as_csv(self, request, queryset):
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
        "voximplant-agent calls"
    )
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([
            obj.id, obj.created_at, obj.updated_at, obj.state,
            obj.connected_form.contract.patient_name,
            obj.connected_form.contract.patient_phone,
        ])

    return response


@admin.register(models.call.Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('id', 'connected_form', 'state', 'created_at')
    list_filter = ('state',)
    readonly_fields = ('created_at', 'updated_at')
    actions = [export_as_csv]


@admin.register(models.ConnectedForm)
class ConnectedFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract', 'form', 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('is_active',)
