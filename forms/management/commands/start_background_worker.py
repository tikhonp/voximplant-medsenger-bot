import sched
import time

from django.core.management.base import BaseCommand

from forms.management.commands._tasks import check_current_calls

REPEAT_DELAY_SECONDS = 60


class Command(BaseCommand):
    help = 'Start worker for executing calls at specific time.'

    def _task(self, scheduler):
        scheduler.enter(REPEAT_DELAY_SECONDS, 1, self._task, (scheduler,))
        check_current_calls()

    def handle(self, *args, **options):
        if options['one_shot']:
            check_current_calls()
            return
        my_scheduler = sched.scheduler(time.time, time.sleep)
        my_scheduler.enter(REPEAT_DELAY_SECONDS, 1, self._task, (my_scheduler,))
        my_scheduler.run()

    def add_arguments(self, parser):
        parser.add_argument(
            '-o',
            '--one-shot',
            action='store_true',
            default=False,
            help='Run worker only once.'
        )
