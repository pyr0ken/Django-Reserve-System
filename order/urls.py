from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('date/<int:year>/<int:month>/<int:day>/time/<int:hour>/<int:minute>', views.OrderDetail.as_view(),
         name='order_page')
]
