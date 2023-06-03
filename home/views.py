from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model


class HomeView(TemplateView):
    template_name = 'home/index.html'
    user_model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['me'] = self.user_model.objects.first()
        return context
