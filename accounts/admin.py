from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'is_active']
    list_filter = ['is_active']
    list_editable = ['is_active', 'phone_number']
    search_fields = ['full_name', 'phone_number']
    readonly_fields = ['password', 'date_joined', 'last_login']


admin.site.register(User, UserAdmin)
