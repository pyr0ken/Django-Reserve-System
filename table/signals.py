from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from .models import ReserveDateTime, PriceSetting


@receiver(post_save, sender=PriceSetting)
def set_reserve_date_price(sender, instance: PriceSetting, **kwargs):
    new_price = instance.price
    reserve_weekday = instance.weekdays
    reserve_time = instance.times

    if reserve_weekday == 'All':
        # If reserve_weekday is 'All', we don't need to filter by week_day
        filter_q = Q()
    else:
        # Filter ReserveDateTime instances by week_day
        filter_q = Q(date__week_day=int(reserve_weekday))

    if reserve_time != 'All':
        # If reserve_time is not 'All', filter by time as well
        filter_q &= Q(time__exact=reserve_time)

    # Update all active ReserveDateTime instances that match the filter
    ReserveDateTime.objects.filter(filter_q, is_active=True).update(price=new_price)

    # reserve_dates = ReserveDateTime.objects.filter(is_active=True)
    #
    # if reserve_weekday == 'All':
    #     if reserve_time == 'All':
    #         reserve_dates.update(price=new_price)
    #     else:
    #         reserve_dates.filter(time__exact=reserve_time).update(price=new_price)
    # else:
    #     if reserve_time == 'All':
    #         reserve_dates.filter(date__week_day=int(reserve_weekday)).update(price=new_price)
    #     else:
    #         reserve_dates.filter(date__week_day=int(reserve_weekday), time__exact=reserve_time).update(price=new_price)
