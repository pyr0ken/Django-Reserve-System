from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordChangeForm
from .models import User
from .validators import is_valid_phone_number


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='پسورد', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار پسورد', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'phone_number', 'password')

    def clean_password2(self):
        cd = self.cleaned_data
        password1 = cd['password1']
        password2 = cd['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError('رمز ها یکشان نمیباشند!')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="شما میتوانید با استفاده از این <a href=\"../password/\">لینک</a> پسورد خود را تفییر دهید.")

    class Meta:
        model = User
        fields = ('full_name', 'phone_number', 'password')


class RegisterForm(forms.Form):
    full_name = forms.CharField(
        label="نام و نام خانوادگی",
        max_length=200,
        error_messages={
            'required': 'این فیلد اجباری است.'
        }
    )
    phone_number = forms.CharField(
        label='شماره موبایل',
        validators=[
            is_valid_phone_number,
        ],
        error_messages={
            'required': 'این فیلد اجباری است.'
        }
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(8),
        ],
        error_messages={
            'required': 'این فیلد اجباری است.'
        }
    )
    confirm_password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(8),
        ],
        error_messages={
            'required': 'این فیلد اجباری است.'
        }
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('رمز عبور و تکرار رمز عبور یکسان نیستند.')


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        label='شماره موبایل',
        validators=[
            is_valid_phone_number
        ],
        error_messages={
            'required': 'این فیلد اجباری است.'
        }
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100)
        ],
        error_messages={
            'required': 'این فیلد اجباری است.'
        }
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='رمز قبلی',
        widget=forms.PasswordInput,
        validators=[
            validators.MaxLengthValidator(100),
        ],
        error_messages={
            'required': 'این فیلد اجباری است.'
        }
    )
    new_password1 = forms.CharField(
        label='رمز جدید',
        widget=forms.PasswordInput,
        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(8),
        ],
        error_messages={
            'required': 'این فیلد اجباری است.'
        }
    )
    new_password2 = forms.CharField(
        label='تکرار رمز جدید',
        widget=forms.PasswordInput,
        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(8),
        ],
        error_messages={
            'required': 'این فیلد اجباری است.'
        }
    )

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('رمز قبلی نادرست است.')
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('رمز جدید و تکرار آن یکسان نیستند.')
        return new_password2


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number']
