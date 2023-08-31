from __future__ import annotations

from datetime import datetime, timedelta
from datetime import time as python_time

from django.db import models

from medsenger_agent.models import Contract


class TimeSlot(models.Model):
    """Available time slot that patient accepts for call."""

    time = models.TimeField()

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='time_slot_set')

    class Meta:
        ordering = ('time',)

    @staticmethod
    def get_next_timeslot(from_date: datetime, contract: Contract) -> ((python_time | None), bool):
        """
        Get next available time slot, returns time and flag if that time is tomorrow, otherwise now.
        If contract's timezone_offset is not None time will be localized.
        """

        time_slots = TimeSlot.objects.filter(contract=contract)

        for time_slot in time_slots:
            if time_slot.time > from_date.time():
                if contract.timezone_offset is not None:
                    localized_date = (datetime.combine(datetime.now().date(), time_slot.time) -
                                      timedelta(minutes=contract.timezone_offset))
                    return localized_date.time(), False
                else:
                    return time_slot.time, False

        time_slot = time_slots.first()
        if time_slot is not None:
            if contract.timezone_offset is not None:
                localized_date = (datetime.combine(datetime.now().date(), time_slot.time) -
                                  timedelta(minutes=contract.timezone_offset))
                return localized_date.time(), True
            else:
                return time_slot.time, True

        return None, False
