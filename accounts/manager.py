from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, full_name, email, password, *args, **kwargs):
        if not email:
            raise ValueError('User must have a phone number.')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, email, password, *args, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email),
            full_name=full_name,
            password=password,
        )
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
