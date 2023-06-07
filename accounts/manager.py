from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, full_name, phone_number, national_code, password, *args, **kwargs):
        if not phone_number:
            raise ValueError('User must have a phone number.')

        user = self.model(
            phone_number=phone_number,
            national_code=national_code,
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, phone_number, national_code, password, *args, **kwargs):
        user = self.create_user(
            phone_number=phone_number,
            full_name=full_name,
            national_code=national_code,
            password=password,
        )
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
