from django.shortcuts import render
from django.views import View


class OrderView(View):
    def get(self, request):
        template_name = 'order/reserve_page.html'

        return render(request, template_name, {})

    def post(self, request):
        pass
