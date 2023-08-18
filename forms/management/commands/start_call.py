from django.core.management import BaseCommand

from forms.management.commands._tasks import start_call


class Command(BaseCommand):
    help = 'Start call for specific contract and form.'

    def add_arguments(self, parser):
        parser.add_argument("--contract_id", required=True, type=int)
        parser.add_argument("--form_id", required=True, type=int)

    def handle(self, *args, **options):
        start_call(options['contract_id'], options['form_id'])
