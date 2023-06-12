from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager
from .validators import is_valid_phone_number


class User(AbstractBaseUser):
    full_name = models.CharField(
        verbose_name="نام و نام خانوادگی",
        max_length=200
    )
    phone_number = models.CharField(
        verbose_name='شماره موبایل',
        validators=[is_valid_phone_number],
        unique=True
    )

    # required
    date_joined = models.DateTimeField(verbose_name="تاریخ ثبت نام",auto_now_add=True, editable=False)
    last_login = models.DateTimeField(verbose_name="تاریخ اخرین ورود",auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    class Meta:
        db_table = 'reserve_system_accounts'
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
