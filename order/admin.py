from django.contrib import admin
from jalali_date import datetime2jalali
from jalali_date.fields import JalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget
from django.db import models
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'reserve_date', 'is_paid', 'jalali_payment_date']
    list_filter = ['is_paid', 'payment_date']
    search_fields = ['is_paid', 'payment_date']
    list_editable = ['is_paid']
    # readonly_fields = ['jalali_payment_date']

    formfield_overrides = {
        models.DateTimeField: {
            'form_class': JalaliDateTimeField,
            'widget': AdminJalaliDateWidget,
        },
    }

    def jalali_payment_date(self, obj):
        return datetime2jalali(obj.payment_date).strftime("%d/ %m / %Y %H:%M:%S")

    jalali_payment_date.short_description = "تاریخ پرداخت"


admin.site.register(Order, OrderAdmin)
