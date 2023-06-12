import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View
from django.contrib import messages
from jalali_date import date2jalali
from jdatetime import JalaliToGregorian
from table.models import ReserveDateTime
from utils.get_weekday_current_number import get_weekday_current_number
from utils.get_current_time import get_current_time
from .forms import OrderAddForm
from .models import Order
from .zarinpal import payment_request, payment_verification, ZarinpalError


class OrderPayView(View):
    template_name = 'order/reserve_page.html'

    def setup(self, request, *args, **kwargs):
        year = kwargs.get('year')
        month = kwargs.get('month')
        day = kwargs.get('day')
        hour = kwargs.get('hour')
        minute = kwargs.get('minute')

        today = get_current_time()
        date = JalaliToGregorian(year, month, day).getGregorianList()  # -> tuple(year, month, day)
        reserve_current_date = datetime.date(date[0], date[1], date[2])

        if reserve_current_date < today.date():
            raise Http404

        self.reserve_date = get_object_or_404(ReserveDateTime,
                                              status='AVA',
                                              is_active=True,
                                              date__year=date[0],
                                              date__month=date[1],
                                              date__day=date[2],
                                              time__hour=hour,
                                              time__minute=minute)

        reserve_date_weekday = self.reserve_date.date.weekday()
        reserve_date_current_weekday = get_weekday_current_number(reserve_date_weekday)

        self.reserve_current_count = ReserveDateTime.objects.filter(
            date__gte=self.reserve_date.date,
            date__week_day=reserve_date_current_weekday,
            time__exact=self.reserve_date.time,
        ).count()

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
            'reserve_form': reserve_form,
            'reserve_current_count': self.reserve_current_count
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        reserve_form = OrderAddForm(request.POST)
        if reserve_form.is_valid():
            reserve_count = reserve_form.cleaned_data.get("reserve_count")

            # Check count is an integer.
            if reserve_count not in range(1, self.reserve_current_count + 1):
                reserve_form.add_error('reserve_count', "تعداد جلسات وارد شده معتبر نمی باشد.")
            else:
                amount = self.reserve_date.price * reserve_count
                reserve_date_jalali = str(date2jalali(self.reserve_date.date))
                description = f'شما درحال رزرو سانس ورزشی با تاریخ {reserve_date_jalali} و زمان {self.reserve_date.time} هستید. با تشکر - سامانه رزرو سالن'
                mobile = request.user.phone_number
                try:
                    new_order = Order(
                        user_id=request.user.id,
                        reserve_date=self.reserve_date,
                        reserve_count=reserve_count,
                        final_price=amount,
                        is_paid=False,
                    )
                    # try to create payment if success get url to redirect it
                    redirect_url = payment_request(amount, description, mobile=mobile, order=new_order)

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

                code, message, ref_id = payment_verification(order.final_price, authority)

                # everything is okey
                if code == 100:
                    order.reference_id = ref_id
                    order.is_paid = True
                    order.save()
                    for count in range(1, order.reserve_count + 1):
                        order_weekday = order.reserve_date.date.weekday()
                        order_current_weekday = get_weekday_current_number(order_weekday)
                        order_reserve_date = ReserveDateTime.objects.filter(
                            date__gte=order.reserve_date.date,
                            date__week_day=order_current_weekday,
                            time__exact=order.reserve_date.time,
                            status__exact='AVA',
                            is_active=True,
                        ).order_by('date').first()
                        order_reserve_date.status = 'BOK'
                        order_reserve_date.save()

                    content = {
                        'type': 'Success',
                        'ref_id': ref_id
                    }
                    messages.success(request, f'پرداخت با موفیقت انجام شد. کد رهگیری {ref_id}')
                    return redirect('home:home')

                # operation was successful but PaymentVerification operation on this transaction have already been done
                elif code == 101:
                    content = {
                        'type': 'Warning'
                    }
                    messages.error(request, f'پرداخت با خطا مواجه شد.')
                    return redirect('home:home')

            # if got an error from zarinpal
            except ZarinpalError as e:
                return HttpResponse(e)

        messages.error(request, f'پرداخت با خطا مواجه شد.')
        return redirect('home:home')
