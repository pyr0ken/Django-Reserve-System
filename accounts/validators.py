import re
from django.core.exceptions import ValidationError


def is_valid_national_code(national_code):
    if not re.match(r'^(?!(\d)\1{9})\d{10}$', str(national_code)):
        raise ValidationError('لطفا کد ملی معتبر وارد کنید.')


def is_valid_phone_number(phone_number):
    if not re.match(r'^۰۹[۰-۹]{9}$|^09[0-9]{9}$', str(phone_number)):
        raise ValidationError('لطفا شماره موبایل معتبر وارد کنید.')
