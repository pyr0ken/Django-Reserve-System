from django.core.management.base import BaseCommand
from table.create_reservation import create_reservations


class Command(BaseCommand):
    help = 'Creates reservations for the next 30 days'

    def handle(self, *args, **options):
        create_reservations()
        self.stdout.write(self.style.SUCCESS('Reservations created successfully.'))
