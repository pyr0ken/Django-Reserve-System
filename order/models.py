from django.db import models
from django.conf import settings
from table.models import ReserveDateTime
from django.core.validators import MinValueValidator


class Order(models.Model):
    authority = models.BigIntegerField(primary_key=True)
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
        verbose_name='پرداخت شده/نشده',
        default=False,
    )
    payment_date = models.DateTimeField(
        verbose_name='تاریخ پرداخت',
        auto_now_add=True,
    )
    reserve_count = models.PositiveSmallIntegerField(
        verbose_name='تعداد جلسات رزرو',
        default=1,
        validators=[MinValueValidator(1)],
    )
    reference_id = models.IntegerField(
        verbose_name='کد رهگیری',
        blank=True,
        null=True
    ),
    final_price = models.DecimalField(
        verbose_name="قیمت",
        max_digits=10,
        decimal_places=0,
        default=0,
        help_text="لطفا هزینه رزرو را به <strong>تومان</strong> وارد کنید."
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
