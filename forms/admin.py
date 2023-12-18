from django.contrib import admin

from forms import models


@admin.register(models.Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('name', 'scenario_id', 'is_active')


@admin.register(models.TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('time', 'connected_form')


@admin.register(models.call.Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('id', 'connected_form', 'state', 'created_at',)
    list_filter = ('state',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(models.ConnectedForm)
class ConnectedFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract', 'form', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
