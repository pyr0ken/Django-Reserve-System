from datetime import datetime, timedelta
from django.http import HttpRequest, Http404
from django.shortcuts import render
from utils.get_current_time import get_current_time
from .models import ReserveDateTime


def week_data(request: HttpRequest, week_number: int):
    if not 0 < week_number < 5:
        raise Http404

    today = get_current_time()
    start_time = today.date() + timedelta(days=7 * (week_number - 1))
    end_time = start_time + timedelta(days=6)

    # Get days from a week number.
    reserve_days = ReserveDateTime.objects.filter(date__range=(start_time, end_time), is_active=True)

    # Change expired days status to unavailable
    # reserve_days.filter(date=today, status='AVA', time__lte=today.time()).update(status='UNA')
    for reserve_day in reserve_days:
        if reserve_day.date == today.date() and reserve_day.status == 'AVA' and reserve_day.time <= today.time():
            reserve_day.status = 'UNA'
            reserve_day.save()

    # Get reserve times
    reserve_times = [choice[0] for choice in ReserveDateTime.Time.choices]

    # Get date of the days for table header
    reserve_days_header = sorted(set(day.date for day in reserve_days))

    context = {
        'reserve_days': reserve_days,
        'reserve_times': reserve_times,
        'reserve_days_header': reserve_days_header,
    }

    return render(request, 'table/table.html', context)
