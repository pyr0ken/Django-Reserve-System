from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),
    path('profile/reserve-history/', views.ProfileReserveHistoryView.as_view(), name='reserve_history_page'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='edit_profile_page'),
    path('profile/change-password/', views.ProfileChangePasswordView.as_view(), name='change_password_page'),
]
