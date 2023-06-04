from datetime import timedelta
from django.http import HttpRequest
from django.utils import timezone
from django.shortcuts import render
from django.conf import settings
from .models import ReserveDateTime


def week_data(request: HttpRequest, week_number: int):
    start_time = timezone.now().astimezone(settings.IRAN_TIME_ZONE).date() + timedelta(days=7 * (week_number - 1))
    end_time = start_time + timedelta(days=6)

    # Get the
    reserve_days_header_list = [start_time + timedelta(days=i) for i in range(7)]

    # Get days from a week number.
    reserve_days = ReserveDateTime.objects.filter(date__range=(start_time, end_time))

    """ Get days data for table header :
            - filter date for get this week number. 
            - just get a date value. 
            - use distinct function for delete duplicate days. """
    reserve_days_header = ReserveDateTime.objects.filter(date__in=reserve_days_header_list).values_list('date',
                                                                                                        flat=True).distinct()

    context = {
        'reserve_days': reserve_days,
        'reserve_days_header': reserve_days_header,
    }

    return render(request, 'table/table.html', context)
