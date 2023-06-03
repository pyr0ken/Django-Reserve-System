from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'email', 'is_active']
    list_filter = ['is_active']
    list_editable = ['is_active', 'phone_number', 'email']
    search_fields = ['full_name', 'phone_number', 'email']
    readonly_fields = ['password']


admin.site.register(User, UserAdmin)
