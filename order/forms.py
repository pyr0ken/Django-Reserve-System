from django import forms
from accounts.validators import is_valid_national_code


class OrderAddForm(forms.Form):
    national_code = forms.CharField(
        label="کد ملی",
        validators=[is_valid_national_code],
        error_messages={
            'required': 'لطفا کد ملی خود را وارد کنید.'
        }
    )
    reserve_count = forms.IntegerField(
        label="تعداد جلسات رزرو",
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 4}),
        initial=1
    )
