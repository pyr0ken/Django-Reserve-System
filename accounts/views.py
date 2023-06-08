from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import User
from django.utils.crypto import get_random_string
from django.http import Http404, HttpRequest, JsonResponse
from django.contrib.auth import login, logout, authenticate
from utils.email_service import send_email
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from persiantools import digits


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }

        return render(request, 'accounts/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_full_name = register_form.cleaned_data.get('full_name')
            user_phone_number = register_form.cleaned_data.get('phone_number')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(phone_number__iexact=user_phone_number).exists()
            if user:
                register_form.add_error('phone_number', 'شماره موبایل وارد شده در سایت ثبت نام کرده است!')
            else:
                new_user = User(
                    full_name=user_full_name,
                    phone_number=user_phone_number,
                    is_active=True,
                )
                new_user.set_password(user_password)
                new_user.save()
                messages.success(request, 'ثبت نام با موفقیت انجام شد. اکنون میتوانید وارد سایت شوید!')

        context = {
            'register_form': register_form
        }

        return render(request, 'accounts/register.html', context)


# class ActivateAccountView(View):
#     def get(self, request, email_active_code):
#         user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
#         if user is not None:
#             if not user.is_active:
#                 user.is_active = True
#                 user.email_active_code = get_random_string(72)
#                 user.save()
#                 # todo: show success message to user
#                 return redirect(reverse('login_page'))
#             else:
#                 # todo: show your account was activated message to user
#                 pass
#
#         raise Http404


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }

        return render(request, 'accounts/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_phone_number = login_form.cleaned_data.get('phone_number')
            user_password = login_form.cleaned_data.get('password')
            user_phone_number = digits.fa_to_en(user_phone_number)
            user = authenticate(request, phone_number=user_phone_number, password=user_password)
            if user is not None:
                login(request, user)
                messages.success(request, f"{user.full_name} عزیز خوش آمدید!")
                return redirect(reverse('home:home'))
            else:
                messages.error(request, 'کاربری با مشخصات وارد شده یافت نشد.')

        context = {
            'login_form': login_form
        }

        return render(request, 'accounts/login.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('home:home'))
#
# class ForgetPasswordView(View):
#     def get(self, request: HttpRequest):
#         forget_pass_form = ForgotPasswordForm()
#         context = {'forget_pass_form': forget_pass_form}
#         return render(request, 'accounts/forgot_password.html', context)
#
#     def post(self, request: HttpRequest):
#         forget_pass_form = ForgotPasswordForm(request.POST)
#         if forget_pass_form.is_valid():
#             user_email = forget_pass_form.cleaned_data.get('email')
#             user: User = User.objects.filter(email__iexact=user_email).first()
#             if user is not None:
#                 send_email('بازیابی کلمه عبور', user.email, {'user': user}, 'emails/forgot_password.html')
#                 return redirect(reverse('home_page'))
#
#         context = {'forget_pass_form': forget_pass_form}
#         return render(request, 'accounts/forgot_password.html', context)
#
#
# class ResetPasswordView(View):
#     def get(self, request: HttpRequest, active_code):
#         user: User = User.objects.filter(email_active_code__iexact=active_code).first()
#         if user is None:
#             return redirect(reverse('login_page'))
#
#         reset_pass_form = ResetPasswordForm()
#
#         context = {
#             'reset_pass_form': reset_pass_form,
#             'user': user
#         }
#         return render(request, 'accounts/reset_password.html', context)
#
#     def post(self, request: HttpRequest, active_code):
#         reset_pass_form = ResetPasswordForm(request.POST)
#         user: User = User.objects.filter(email_active_code__iexact=active_code).first()
#         if reset_pass_form.is_valid():
#             if user is None:
#                 return redirect(reverse('login_page'))
#             user_new_pass = reset_pass_form.cleaned_data.get('password')
#             user.set_password(user_new_pass)
#             user.email_active_code = get_random_string(72)
#             user.is_active = True
#             user.save()
#             return redirect(reverse('login_page'))
#
#         context = {
#             'reset_pass_form': reset_pass_form,
#             'user': user
#         }
#
#         return render(request, 'accounts/reset_password.html', context)
