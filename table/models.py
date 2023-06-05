from datetime import time, datetime
from django.db import models
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
        verbose_name="هزینه",
        max_digits=10,
        decimal_places=0,
        null=True,
        blank=True,
        help_text="لطفا هزینه رزرو را به <strong>تومان</strong> وارد کنید."
    )

    class Meta:
        db_table = "reserve_system_table_time"
        ordering = ['date']
        verbose_name = "روز رزرو"
        verbose_name_plural = "روز های رزرو"

    def __str__(self):
        return f'weekday: {self.get_weekday()} | date: {date2jalali(self.date).strftime("%Y/%m/%d")} | time: {self.time}'

    # def get_absolute_url(self):
    #     pass

    def get_weekday(self):
        days_of_week = ['دوشنبه', 'سه شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه', 'یکشنبه']
        date = datetime.strptime(str(self.date), '%Y-%m-%d')
        weekday = date.weekday()
        weekday_name = days_of_week[weekday]
        return weekday_name

    get_weekday.short_description = "روز هفته"
