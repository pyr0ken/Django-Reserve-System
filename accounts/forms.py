from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='پسورد', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار پسورد', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'email_active_code', 'phone_number', 'password')

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
        fields = ('full_name', 'email', 'email_active_code', 'phone_number', 'password')

#
# class RegisterForm(forms.Form):
#     email = forms.EmailField(
#         label='ایمیل',
#         widget=forms.EmailInput(),
#         validators=[
#             validators.MaxLengthValidator(100),
#             validators.EmailValidator,
#         ]
#     )
#     password = forms.CharField(
#         label='کلمه عبور',
#         widget=forms.PasswordInput(),
#         validators=[
#             validators.MaxLengthValidator(100),
#         ]
#     )
#     confirm_password = forms.CharField(
#         label='تکرار کلمه عبور',
#         widget=forms.PasswordInput(),
#         validators=[
#             validators.MaxLengthValidator(100),
#         ]
#     )
#
#     def clean_confirm_password(self):
#         password = self.cleaned_data.get('password')
#         confirm_password = self.cleaned_data.get('confirm_password')
#
#         if password == confirm_password:
#             return confirm_password
#
#         raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')


# class LoginForm(forms.Form):
#     email = forms.EmailField(
#         label='ایمیل',
#         widget=forms.EmailInput(),
#         validators=[
#             validators.MaxLengthValidator(100),
#             validators.EmailValidator
#         ]
#     )
#     password = forms.CharField(
#         label='کلمه عبور',
#         widget=forms.PasswordInput(),
#         validators=[
#             validators.MaxLengthValidator(100)
#         ]
#     )
#
#
# class ForgotPasswordForm(forms.Form):
#     email = forms.EmailField(
#         label='ایمیل',
#         widget=forms.EmailInput(),
#         validators=[
#             validators.MaxLengthValidator(100),
#             validators.EmailValidator
#         ]
#     )
#
#
# class ResetPasswordForm(forms.Form):
#     password = forms.CharField(
#         label='کلمه عبور',
#         widget=forms.PasswordInput(),
#         validators=[
#             validators.MaxLengthValidator(100),
#         ]
#     )
#
#     confirm_password = forms.CharField(
#         label='تکرار کلمه عبور',
#         widget=forms.PasswordInput(),
#         validators=[
#             validators.MaxLengthValidator(100),
#         ]
#     )
