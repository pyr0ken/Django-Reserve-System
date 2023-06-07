from django.shortcuts import render, get_object_or_404
from django.views import View
from table.models import ReserveDateTime


class OrderDetail(View):
    def get(self, request, year, month, day, hour, minute):
        template_name = 'order/reserve_page.html'

        reserve_date = get_object_or_404(ReserveDateTime,
                                         status='AVA',
                                         date__year=year,
                                         date__month=month,
                                         date__day=day,
                                         time__hour=hour,
                                         time__minute=minute)

        context = {
            'reserve_date': reserve_date
        }

        return render(request, template_name, context)

    def post(self, request):
        pass

