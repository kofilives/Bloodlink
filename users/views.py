from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
import jwt
from users.forms import PasswordResetRequestForm
from .models import CustomUser, HospitalUser,Profile
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from decouple import config
from django.urls import reverse
from .utils import send_mail_verification, send_reset_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import userUpdateForm, ProfileUpdateForm, PatientInfoForm,CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from .encryption import encrypt_data, generate_keys, generate_hash
 

# from .crypto_utils import encrypt_data, generate_keys, generate_hash


def account_activated(request):
    return render(
        request, "users/account_activated.html", {"title": "Account Activated"}
    )

@login_required
def userDashboard(request):
    return render(request, "users/userDashboard.html")

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    if request.method == "POST":
        u_form = userUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated')
            return redirect("profile")

    else:
        u_form = userUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/profile.html", context)





def notifications(request):
    return render(request, "users/notifications.html")




def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_verified = False
            user.user_type = form.cleaned_data['role']
            # private_key, public_key = generate_keys()
            # iv, ciphertext, tag = encrypt_data(public_key, str(user))
            # user.encrypted_data = ciphertext.hex()
            user.save()
            
            # data_hash = generate_hash(ciphertext)
            # add_data_to_blockchain(user.user_id, data_hash)
            

            user = CustomUser.objects.get(email=form.cleaned_data["email"])
            token = jwt.encode(
                {"user_id": user.id}, config("SECRET_KEY"), algorithm="HS256"
            )
            current_site = get_current_site(request).domain
            relative_link = reverse("verify_user")
            absolute_url = f"http://{current_site}{relative_link}?token={token}"
            link = str(absolute_url)
            send_mail_verification(email=user.email, link=link)

            messages.success(
                request,
                "Your account has been created! Please verify your email and log in.",
            )
            return render(request, "users/account_activation_sent.html")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/signup.html", {"form": form, "title": "Sign Up"})


def verify_user(request):
    token = request.GET.get("token")

    try:
        payload = jwt.decode(token, config("SECRET_KEY"), algorithms=["HS256"])
        user = CustomUser.objects.get(id=payload["user_id"])

        if not user.is_verified:
            user.is_active = True
            user.is_verified = True
            user.save()
            messages.success(request, "Email verified, you may now log in.")
            return render(request, "users/account_activated.html")
        else:
            messages.success(request, "Email already verified, you may now log in.")
            return render(request, "users/account_already_activated.html")
    except jwt.ExpiredSignatureError or jwt.DecodeError or jwt.InvalidTokenError:
        return render(request, "users/account_activation_invalid.html")


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
    return redirect("login")


class CustomLoginView(LoginView):
    authentication_form = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        if user.is_active and user.is_verified:
            login(self.request, user)
            if user.role == 'hospitals':
                HospitalUser.objects.get_or_create(user=user)
                return render(self.request, "hospitals/hospitalDashboard.html")
            else:  # Assuming the other option is 'custom'
                return render(self.request, "users/userDashboard.html")
        elif user.is_active and not user.is_verified:
            messages.error(self.request, "Please verify your email before logging in.")
            return redirect("login")
        else:
            messages.error(self.request, "There is no account with this email. Please sign up.")
            return redirect("signup")


def update_user(request):
    if request.method == "POST":
        form = userUpdateForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect(
                "profile"
            )  # Redirect to a success page or wherever you want
    else:
        form = userUpdateForm()
    return render(request, "profile.html", {"form": form})

def patient_info(request):
    if request.method == "POST":
        form = PatientInfoForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect(
                "patient_info_success"
            )  # Redirect to a success page or wherever you want
    else:
        form = PatientInfoForm()
    return render(request, "hospitals/donorInformation.html", {"form": form})



def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_success')
    return render(request, 'users/appointment.html')


def appointment_success(request):
    return render(request, 'users/appointment_success.html')