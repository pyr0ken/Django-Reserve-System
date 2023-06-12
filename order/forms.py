from django import forms


class OrderAddForm(forms.Form):
    reserve_count = forms.IntegerField(
        label="تعداد جلسات رزرو",
        widget=forms.NumberInput(attrs={'type': 'range'}),
        initial=1
    )
