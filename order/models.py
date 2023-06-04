from django.db import models
from django.conf import settings
from utils.get_current_time import get_current_time
from table.models import ReserveDateTime


class Order(models.Model):
    user = models.ForeignKey(
        verbose_name='کاربر',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_orders')
    reserve_date = models.ForeignKey(
        verbose_name='تاریخ رزرو',
        to=ReserveDateTime,
        on_delete=models.CASCADE,
        related_name='reserve_date_orders')
    is_paid = models.BooleanField(
        verbose_name='نهایی شده/نشده'
    )
    payment_date = models.DateTimeField(
        verbose_name='تاریخ پرداخت',
        null=True,
        blank=True
    )
    reserve_count = models.PositiveSmallIntegerField(
        verbose_name='تعداد رزرو',
        default=1,
    )

    def __str__(self):
        return f'{self.user} - {self.reserve_date.date} - {self.reserve_date.time}'

    class Meta:
        db_table = 'reserve_system_orders'
        ordering = ['is_paid', '-reserve_date']
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def total_price(self):
        return (self.reserve_date.price * self.reserve_count)
