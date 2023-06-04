from django.contrib import admin
from .models import ReserveDateTime
from django.db import models
from jalali_date import date2jalali
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget


#
class ReserveDateTimeAdmin(admin.ModelAdmin):
    list_display = ['jdate', 'get_weekday', 'time', 'price', 'status']
    list_filter = ['date', 'status', 'time']
    # todo: this isn't work for Date Farsi.
    # search_fields = ['reserve_date', 'reserve_time', 'reserve_price', 'reserve_status']
    # search_help_text = "برای جستجو با نتیجه مناسب تر میتوانید بدین جالت سرچ کنید. روز / ماه / سال به عنوان مثال: 1401/05/01"
    list_editable = ['status']
    formfield_overrides = {
        models.DateField: {
            'form_class': JalaliDateField,
            'widget': AdminJalaliDateWidget,
        },
    }

    def jdate(self, obj):
        return date2jalali(obj.date).strftime("%d/ %m / %Y")

    jdate.short_description = "تاریخ رزرو"


admin.site.register(ReserveDateTime, ReserveDateTimeAdmin)
