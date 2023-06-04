from django.urls import path
from . import views

app_name = 'table'
urlpatterns = [
    path('week/<int:week_number>/', views.week_data, name='week_data'),
]
