from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Runs makemigrations and migrate for a specific app'

    def handle(self, *args, **options):
        call_command('makemigrations')
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Migrations completed successfully'))
