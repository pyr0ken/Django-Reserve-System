from celery import shared_task
from .models import ReserveDateTime
from utils.get_current_time import get_current_time


@shared_task
def check_and_unavailable_date():
    current_time = get_current_time()
    reserve_dates_to_unavailable = ReserveDateTime.objects.filter(
        date__exact=current_time.date(),
        time__lte=current_time.time(),
        status__exact='AVA')
    if reserve_dates_to_unavailable:
        for reserve_date in reserve_dates_to_unavailable:
            reserve_date.status = 'UNA'
            reserve_date.save()


