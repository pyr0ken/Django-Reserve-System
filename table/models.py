from django.db import models
from django.urls import reverse
from datetime import time, datetime
from jalali_date import date2jalali
from utils.get_current_time import get_current_time


class ReserveDateTime(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'AVA', 'قابل رزرو'
        UNAVAILABLE = 'UNA', 'غیر قابل رزرو'
        BOOKED = 'BOK', 'رزرو شده'

    class Time(time, models.Choices):
        T1 = 1, 30, '01:30'
        T2 = 7, 30, '07:30'
        T3 = 9, 0, '09:00'
        T4 = 10, 30, '10:30'
        T5 = 12, 0, '12:00'
        T6 = 13, 30, '13:30'
        T7 = 15, 0, '15:00'
        T8 = 16, 30, '16:30'
        T9 = 18, 0, '18:00'
        T10 = 19, 30, '19:30'
        T11 = 21, 0, '21:00'
        T12 = 22, 30, '22:30'
        T13 = 23, 59, '23:59'

    date = models.DateField(
        verbose_name="تاریخ",
        default=get_current_time,
        db_index=True
    )
    time = models.TimeField(
        verbose_name="زمان",
        choices=Time.choices,
        db_index=True
    )
    status = models.CharField(
        verbose_name="وضعیت",
        max_length=10,
        choices=Status.choices,
        default=Status.AVAILABLE,
        db_index=True,
    )
    price = models.DecimalField(
        verbose_name="قیمت",
        max_digits=10,
        decimal_places=0,
        default=0,
        help_text="لطفا هزینه رزرو را به <strong>تومان</strong> وارد کنید."
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        db_table = "reserve_system_table"
        ordering = ['date']
        verbose_name = "روز رزرو"
        verbose_name_plural = "روز های رزرو"

    def __str__(self):
        return f'weekday: {self.get_weekday()} | date: {date2jalali(self.date).strftime("%Y/%m/%d")} | time: {self.time}'

    def get_absolute_url(self):
        year = date2jalali(self.date).year
        month = date2jalali(self.date).month
        day = date2jalali(self.date).day
        hour = self.time.hour
        minute = self.time.minute
        return reverse('order:order_pay', args=[year, month, day, hour, minute])

    def get_weekday(self):
        days_of_week = ['دوشنبه', 'سه شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه', 'یکشنبه']
        date = datetime.strptime(str(self.date), '%Y-%m-%d')
        weekday = date.weekday()
        weekday_name = days_of_week[weekday]
        return weekday_name

    get_weekday.short_description = "روز هفته"


class PriceSetting(models.Model):
    class ReserveWeekdays(models.TextChoices):
        All = 'All', 'همه روز ها'
        Saturday = '7', 'شنبه ها'
        Sunday = '1', 'یکشنبه ها'
        Monday = '2', 'دوشنبه ها'
        Tuesday = '3', 'سه شنبه ها'
        Wednesday = '4', 'چهارشنبه ها'
        Thursday = '5', 'پنجشنبه ها'
        Friday = '6', 'جمعه ها'

    class ReserveTimes(models.TextChoices):
        All = 'All', 'همه زمان ها'
        T1 = '01:30', '01:30'
        T2 = '07:30', '07:30'
        T3 = '09:00', '09:00'
        T4 = '10:30', '10:30'
        T5 = '12:00', '12:00'
        T6 = '13:30', '13:30'
        T7 = '15:00', '15:00'
        T8 = '16:30', '16:30'
        T9 = '18:00', '18:00'
        T10 = '19:30', '19:30'
        T11 = '21:00', '21:00'
        T12 = '22:30', '22:30'
        T13 = '23:59', '23:59'

    price = models.DecimalField(
        verbose_name="قیمت سانس",
        decimal_places=0,
        max_digits=10,
        help_text="لطفا هزینه رزرو را به <strong>تومان</strong> وارد کنید."
    )

    weekdays = models.CharField(
        verbose_name='انتخاب روز های هفته',
        choices=ReserveWeekdays.choices,
        default=ReserveWeekdays.All,
    )

    times = models.CharField(
        verbose_name="انتخاب زمان های رزرو",
        choices=ReserveTimes.choices,
        default=ReserveTimes.All,
    )

    class Meta:
        db_table = 'reserve_system_price_setting'
        verbose_name = 'تنظیم قیمت رزرو'
        verbose_name_plural = 'تنظیمات قیمت رزرو'

    def __str__(self):
        return f'{self.price} - {self.weekdays} - {self.times}'
