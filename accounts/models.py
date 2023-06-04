from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=200, verbose_name="نام و نام خانوادگی")
    email = models.EmailField(verbose_name="ایمیل", unique=True)
    email_active_code = models.CharField(max_length=100, verbose_name='کد فعالسازی ایمیل')
    phone_number = models.CharField(verbose_name='شماره تلفن', max_length=11, null=True, blank=True, unique=True)
    avatar = models.ImageField(upload_to='uploads/images', verbose_name='تصویر پروفایل', null=True, blank=True)

    # required
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    last_login = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
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

