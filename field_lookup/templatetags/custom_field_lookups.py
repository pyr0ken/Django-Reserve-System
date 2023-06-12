from datetime import datetime
from typing import List
from django import template

register = template.Library()


@register.filter(name='three_digits_currency')
def three_digits_currency(value: int) -> str:
    return '{:,}'.format(value) + ' تومان'

# todo: (: ببین پسر تو یه نابغه ای

#
@register.filter(name='get_weekday')
def get_weekday(value) -> str:
    days_of_week = ['دوشنبه', 'سه شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه', 'یکشنبه']
    date = datetime.strptime(str(value), '%Y-%m-%d')
    weekday = date.weekday()
    weekday_name = days_of_week[weekday]
    return weekday_name
