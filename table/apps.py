from django.apps import AppConfig


class TableConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'table'
    verbose_name = 'ماژول جدول زمانی'

    def ready(self):
        from . import signals