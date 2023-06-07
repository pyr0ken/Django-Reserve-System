from django.shortcuts import render, get_object_or_404
from django.views import View
from table.models import ReserveDateTime
from jdatetime import JalaliToGregorian


class OrderDetail(View):
    def get(self, request, year, month, day, hour, minute):
        template_name = 'order/reserve_page.html'

        date = JalaliToGregorian(year, month, day).getGregorianList()  # -> tuple(year, month, day)

        reserve_date = get_object_or_404(ReserveDateTime,
                                         status='AVA',
                                         date__year=date[0],
                                         date__month=date[1],
                                         date__day=date[2],
                                         time__hour=hour,
                                         time__minute=minute)

        context = {
            'reserve_date': reserve_date
        }

        return render(request, template_name, context)

    def post(self, request):
        pass
