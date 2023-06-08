from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from jalali_date import date2jalali
from jdatetime import JalaliToGregorian
from utils.get_current_time import get_current_time
from table.models import ReserveDateTime
from .forms import OrderAddForm
from .models import Order
from .zarinpal import Zarinpal, ZarinpalError

'''
 if you want to test youre code on your machine without a real transaction
 you able to use zarinpal sandbox like following code
 if you want use in your product, remove sandbox and replace real mercand and callback url then use it!
'''
zarin_pal = Zarinpal('XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX',
                     'http://127.0.0.1:8000/order/verify',
                     sandbox=True)


class OrderPayView(View):
    template_name = 'order/reserve_page.html'

    def setup(self, request, *args, **kwargs):
        year = kwargs.get('year')
        month = kwargs.get('month')
        day = kwargs.get('day')
        hour = kwargs.get('hour')
        minute = kwargs.get('minute')

        date = JalaliToGregorian(year, month, day).getGregorianList()  # -> tuple(year, month, day)

        self.reserve_date = get_object_or_404(ReserveDateTime,
                                              status='AVA',
                                              date__year=date[0],
                                              date__month=date[1],
                                              date__day=date[2],
                                              time__hour=hour,
                                              time__minute=minute)
        super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "برای رزرو سانس ابتدا باید در سایت ثبت نام کنید.")
            return redirect(reverse('table:week_data', args=[1]))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        reserve_form = OrderAddForm()

        context = {
            'reserve_date': self.reserve_date,
            'reserve_form': reserve_form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        reserve_form = OrderAddForm(request.POST)

        if reserve_form.is_valid():
            if request.user.national_code:
                national_code = request.user.national_code
            else:
                national_code = reserve_form.cleaned_data.get("national_code")
                request.user.national_code = national_code
            reserve_count = reserve_form.cleaned_data.get("reserve_count")
            # 1:
            if reserve_count not in [1, 2, 3, 4]:
                reserve_form.add_error('reserve_count', "تعداد جلسات وارد شده معتبر نمی باشد.")
            # 2:
            UserModel = get_user_model()
            user: bool = UserModel.objects.filter(national_code__iexact=national_code).exists()
            if user:
                reserve_form.add_error('national_code', 'این کد ملی در سییستم موجود میباشد.')
            else:
                amount = self.reserve_date.price * reserve_count
                description = f'شما درحال رزرو سانس ورزشی با تاریخ {date2jalali(self.reserve_date.date)} و زمان {self.reserve_date.time} هستید. با تشکر - سامانه رزرو سالن'
                mobile = request.user.phone_number
                try:
                    # try to create payment if success get url to redirect it
                    redirect_url = zarin_pal.payment_request(amount, description, mobile=mobile)

                    new_order = Order(
                        user_id=request.user.id,
                        reserve_date=self.reserve_date,
                        reserve_count=reserve_count,
                        final_price=amount,
                        authority=zarin_pal.authority,
                        is_paid=False,
                    )
                    new_order.save()

                    # redirect user to zarinpal payment gate to paid
                    return redirect(redirect_url)

                # if got error from zarinpal
                except ZarinpalError as e:
                    return HttpResponse(e)

        context = {
            'reserve_date': self.reserve_date,
            'reserve_form': reserve_form,
        }

        return render(request, self.template_name, context)


class OrderVerifyView(View):
    def get(self, request):
        if request.GET.get('Status') == 'OK':
            authority = int(request.GET['Authority'])
            try:
                # try to found transaction
                try:
                    order = Order.objects.get(authority=authority)

                # if we couldn't find the transaction
                except ObjectDoesNotExist:
                    return HttpResponse('we can\'t find this transaction')

                code, message, ref_id = zarin_pal.payment_verification(order.final_price, authority)

                # everything is okey
                if code == 100:
                    order.reference_id = ref_id
                    order.is_paid = True
                    for count in range(1, order.reserve_count + 1):
                        order_weekday = order.reserve_date.date.weekday()
                        ReserveDateTime.objects.filter(date__week_day=order_weekday,
                                                       time__exact=order.reserve_date.time).update(status='BOK')
                    order.save()

                    content = {
                        'type': 'Success',
                        'ref_id': ref_id
                    }
                    return render(request, 'zarinpal/transaction_status.html', context=content)

                # operation was successful but PaymentVerification operation on this transaction have already been done
                elif code == 101:
                    content = {
                        'type': 'Warning'
                    }
                    return render(request, 'zarinpal/transaction_status.html', context=content)

            # if got an error from zarinpal
            except ZarinpalError as e:
                return HttpResponse(e)

        return render(request, 'zarinpal/transaction_status.html')
