from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='hospital_signup'),
    path('verify/', views.verify_hospital, name='verify_hospital'),
    # path('login/', views.custom_login, name='hospital_login'),
    # path('login/', views.CustomLoginView.as_view(template_name='users/login.html'), name='hospital_login'),
    path('logout/', views.custom_logout, name='hospital_logout'),
    
    
    path('patient_info/success/', views.patient_info_success, name='patient_info_success'),
    
    path('password_reset/', views.password_reset, name='hospital_password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm, name='hospital_password_reset_confirm'),
    path('account_activated/', views.account_activated, name='hospital_account_activated'),
]