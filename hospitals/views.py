from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages

# from django.contrib.auth.views import LoginView
# from django.contrib.auth.forms import AuthenticationForm
# from .forms import HospitalCreationForm, HospitalUpdateForm
# from .models import Hospital

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from users.models import CustomUser
from decouple import config
from .utils import send_mail_verification, send_reset_mail
from django.contrib.auth import logout
from .forms import HospitalAdminCreationForm
from users.forms import PasswordResetRequestForm
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import login_required
from users.models import Appointment


def signup(request):
    if request.method == "POST":
        form = HospitalAdminCreationForm(request.POST)
        if form.is_valid():
            hospital = form.save(commit=False)
            hospital.is_active = True
            hospital.is_verified = False
            hospital.save()

            hospital = CustomUser.objects.get(email=form.cleaned_data["email"])
            token = jwt.encode(
                {"hospital_id": hospital.id}, config("SECRET_KEY"), algorithm="HS256"
            )
            current_site = get_current_site(request).domain
            relative_link = reverse("verify_hospital")
            absolute_url = f"http://{current_site}{relative_link}?token={token}"
            link = str(absolute_url)
            send_mail_verification(email=hospital.email, link=link)

            messages.success(
                request, "Hospital registered successfully! Please verify the email."
            )
            return render(request, "hospitals/account_activation_sent.html")
    else:
        form = HospitalAdminCreationForm()
    return render(request, "hospitals/signup.html", {"form": form})


def verify_hospital(request):
    token = request.GET.get("token")
    try:
        payload = jwt.decode(token, config("SECRET_KEY"), algorithms=["HS256"])
        hospital = CustomUser.objects.get(id=payload["hospital_id"])
        if not hospital.is_verified:
            hospital.is_verified = True
            hospital.save()
            messages.success(request, "Hospital email verified successfully.")
        else:
            messages.info(request, "Hospital email already verified.")
        return render(request, "hospitals/account_already_verified.html")
    except jwt.ExpiredSignatureError or jwt.DecodeError or jwt.InvalidTokenError:
        return render(request, "hospitals/account_activation_invalid.html")


def password_reset(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = CustomUser.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request).domain
                relative_link = reverse(
                    "password_reset_confirm", kwargs={"uidb64": uid, "token": token}
                )
                absolute_url = f"http://{current_site}{relative_link}"
                link = str(absolute_url)

                send_reset_mail(email=user.email, link=link)

                return redirect("password_reset_done")
            else:
                messages.error(request, "No user found with that email address.")
    else:
        form = PasswordResetRequestForm()
    return render(request, "users/password_reset.html", {"form": form})


def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect("login")
        else:
            form = SetPasswordForm(user)
        return render(request, "users/password_reset_confirm.html", {"form": form})
    else:
        messages.error(
            request,
            "The password reset link was invalid, possibly because it has already been used.",
        )
        return render(request, "users/password_reset_invalid.html")


def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("hospital_login")


@login_required
def hospitalDashboard(request):
    return render(request, "hospitals/hospitalDashboard.html")


@login_required
def patient_info(request):
    return render(request, "hospitals/donorInformation.html")


def account_activated(request):
    return render(
        request, "users/account_activated.html", {"title": "Account Activated"}
    )
    
def patient_info_success(request):
    return render(request, 'hospitals/patient_info_success.html')

def info_update_success(request):
    return render(request, 'hospitals/infoUpdate_success.html')


def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'hospitals/appointment_list.html', {'appointments': appointments})

# def patient_info(request):
#     if request.method == 'POST':
#         form = PatientInfoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('patient_info_success')
#     else:
#         form = PatientInfoForm()
#     return render(request, 'hospitals/donorInformation.html', {'form': form})



@login_required
def update_user_info(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        user = get_object_or_404(CustomUser, email=email)

        if user:
            # Update user information based on the provided form data
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.gender = request.POST.get('gender')
            user.age = request.POST.get('age')
            user.date_of_birth = request.POST.get('date_of_birth')
            user.address = request.POST.get('address')
            user.nationality = request.POST.get('nationality')
            user.email = request.POST.get('email')
            user.phone_number = request.POST.get('phone_number')
            user.blood_group = request.POST.get('blood_group')
            user.has_donated_before = request.POST.get('has_donated_before') == 'True'
            user.appointment_date = request.POST.get('date')
            user.appointment_time = request.POST.get('time')
            user.emergency_contact_name = request.POST.get('emergency_contact_name')
            user.emergency_contact_phone = request.POST.get('emergency_contact_phone')
            user.save()

            messages.success(request, 'infoUpdate_success.html')
            return redirect('hospital_dashboard')  # Redirect to the hospital dashboard or any other page

    return render(request, 'donorInformation.html')
