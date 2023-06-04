from django.utils import timezone
from datetime import timedelta
from table_time.models import ReserveDateTime
from django.conf import settings


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def create_booking_dates():
    current_date = timezone.now().astimezone(settings.IRAN_TIME_ZONE).date()
    end_date = current_date + timedelta(days=27)

    reservations = []
    for date in daterange(current_date, end_date):
        for choice in ReserveDateTime.Time.choices:
            time = choice[0]
            reservations.append(ReserveDateTime(date=date, time=time))

    ReserveDateTime.objects.bulk_create(reservations)
