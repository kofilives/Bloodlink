"""
URL configuration for Access_Key_Manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from users import views as users_views
from hospitals import views as hospital_views
from django.contrib.auth import views as auth_views
from project import views
from django.conf import settings
from django.conf.urls.static import static
#from hospitals import views as hospital_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project.urls')),
    path('hospitals/', include('hospitals.urls')),
    path('signup/', users_views.signup, name='signup'),
    path('notifications/', users_views.notifications, name='notifications'),
    path('', views.home, name='home'),
    path('verify-user/', users_views.verify_user, name='verify_user'),
    path('login/', users_views.CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', users_views.custom_logout, name='logout'),
    path('userDashboard/', users_views.userDashboard, name='userDashboard'),
    path("profile/", users_views.profile, name="profile"),
    path("appointment/", users_views.appointment, name="appointment"),
    path('success/', users_views.appointment_success, name='appointment_success'),
    
    path('dashboard/', hospital_views.hospitalDashboard, name='hospital_dashboard'),
    path('patientinfo/', hospital_views.patient_info, name='patientinfo'),
    path('appointments/', hospital_views.appointment_list, name='appointment_list'),
    path('update_user_info/', hospital_views.update_user_info, name='update_user_info'),
    path('info_update_success/', hospital_views.info_update_success, name='info_update_success'),
    
    
    path('password_reset/', users_views.password_reset, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password_reset_done' ,auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name="password_reset_done"),
    path('password_reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name="password_reset_complete"),
    path('account_activated/', users_views.account_activated, name='account_activated'),
]


if settings.DEBUG:
    urlpatterns  += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
 