from .models import ReserveDateTime
from utils.get_current_time import get_current_time
from datetime import timedelta


def add_new_reserve_date():
    yesterday = get_current_time() - timedelta(days=1)
    ReserveDateTime.objects.filter(date__exact=yesterday, is_active=True).update(is_active=False)
    last_reserve_date = ReserveDateTime.objects.last()
    new_reserve_date  = last_reserve_date.date + timedelta(days=1)
    new_reservations = []
    for choice in ReserveDateTime.Time.choices:
        time = choice[0]
        new_reservations.append(ReserveDateTime(date=new_reserve_date, time=time))
    ReserveDateTime.objects.bulk_create(new_reservations)



