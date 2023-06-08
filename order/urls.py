from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('pay/date/<int:year>/<int:month>/<int:day>/time/<int:hour>/<int:minute>', views.OrderPayView.as_view(),
         name='order_pay'),
    path('verify/', views.OrderVerifyView.as_view(), name='order_verify'),
]
