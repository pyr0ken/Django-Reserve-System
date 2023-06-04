from django.core.management.base import BaseCommand
from utils.reserve_dates_generator import create_booking_dates


class Command(BaseCommand):
    help = 'Creates order for the next 30 days'

    def handle(self, *args, **options):
        create_booking_dates()
        self.stdout.write(self.style.SUCCESS('Reservations created successfully.'))
