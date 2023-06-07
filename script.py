def is_valid_melli_code(code):
    try:
        ch_array = [int(ch) for ch in code]
        num2 = ch_array[9]
        if code in [0000000000, 1111111111, "22222222222", "33333333333", "4444444444", "5555555555", "6666666666",
                    "7777777777", "8888888888", "9999999999"]:
            return False
        num3 = sum([(10 - i) * ch_array[i] for i in range(9)])
        num4 = num3 - ((num3 // 11) * 11)
        if (num4 == 0 and num2 == num4) or (num4 == 1 and num2 == 1) or (num4 > 1 and num2 == abs(num4 - 11)):
            return True
        else:
            return False
    except ValueError:
        return False


# validators.py

from django.core.validators import Validator
from django.core.exceptions import ValidationError


class MelliCodeValidator(Validator):
    def __call__(self, value):
        if not is_valid_melli_code(value):
            raise ValidationError('کد ملی نامعتبر است')


# forms.py

from django import forms


class MyForm(forms.Form):
    melli_code = forms.CharField(validators=[MelliCodeValidator()])


# ==============================================

import re
from django.core.exceptions import ValidationError


def validate_number(value):
    if not re.match(r'^[0-9]+$', value):
        raise ValidationError('فقط عدد وارد کنید')


# =====================================================
from django import forms


class MyForm(forms.Form):
    my_field = forms.CharField(validators=[validate_number])
