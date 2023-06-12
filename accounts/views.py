from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from order.models import Order
from persiantools import digits
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .forms import RegisterForm, LoginForm, CustomPasswordChangeForm, EditProfileModelForm
from .models import User


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
            user_phone_number = digits.fa_to_en(user_phone_number)
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


class ProfileReserveHistoryView(View):
    def get(self, request):
        template_name = 'accounts/reserve_history.html'

        user_orders = Order.objects.filter(user_id=request.user.id, is_paid=True)

        context = {
            'user_orders': user_orders,
        }

        return render(request, template_name, context)


# @method_decorator(cache_page(0), name='dispatch')
class ProfileEditView(View):
    template_name = 'accounts/edit_profile.html'

    def get(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(instance=current_user)
        context = {
            'form': edit_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)

        context = {
            'form': edit_form,
        }

        return render(request, self.template_name, context)


class ProfileChangePasswordView(PasswordChangeView):
    success_url = reverse_lazy('accounts:login_page')
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/change_password.html'
