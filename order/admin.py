from django.contrib import admin
from jalali_date import date2jalali
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from django.db import models
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'reserve_date', 'is_paid', 'jalali_payment_date']
    list_filter = ['is_paid', 'payment_date']
    search_fields = ['user', 'reserve_date', 'is_paid', 'payment_date']
    list_editable = ['is_paid']

    formfield_overrides = {
        models.DateField: {
            'form_class': JalaliDateField,
            'widget': AdminJalaliDateWidget,
        },
    }

    def jalali_payment_date(self, obj):
        return date2jalali(obj.peyment_date).strftime("%d/ %m / %Y")

    jalali_payment_date.short_description = "تاریخ رزرو"


admin.register(Order, OrderAdmin)
