import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ReserveDateTime, PriceSetting


@receiver(post_save, sender=PriceSetting)
def set_reserve_date_price(sender, instance: PriceSetting, created: bool, **kwargs):
    if created:
        new_price = instance.price
        weekdays = instance.weekdays
        times = time.strptime(instance.times)

        reserve_dates = ReserveDateTime.objects.filter(is_active=True)

        if weekdays == PriceSetting.ReserveWeekdays.All:
            if time == PriceSetting.ReserveTimes.All:
                reserve_dates.update(price=new_price)
            else:
                reserve_dates.filter(time__exact=times).update(price=new_price)
        else:
            reserve_dates.filter(date__week_day=int(weekdays), time__exact=time).update(price=new_price)


