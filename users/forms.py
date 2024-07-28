from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import Profile
from django.contrib.auth.models import User
from .models import CustomUser,Appointment


class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        
        ('users', 'Custom User'),
        ('hospitals', 'Hospital User'),
    ]
    
    role = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)
    
    class Meta:
        model = CustomUser
        fields = ("role","email", "password1", "password2",)

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "first_name",
            "last_name",
            "national_id",
            "gender",
            "email",
            "phone_number",
            "date",
            "time",
            
            "has_donated_before",
            "terms_agreed",
        ]


class PatientInfoForm(forms.ModelForm):
    ghana_card_id = forms.CharField(max_length=15)
    first_name = forms.CharField(
        max_length=100,
    )
    last_name = forms.CharField(
        max_length=100,
    )
    email = forms.EmailField()
    gender = forms.CharField(
        max_length=10,
    )
    age = forms.IntegerField()
    date_of_birth = forms.DateField()
    address = forms.CharField(
        max_length=255,
    )
    nationality = forms.CharField(
        max_length=100,
    )
    phone_number = forms.CharField(
        max_length=15,
    )
    blood_group = forms.CharField(
        max_length=30,
    )
    emergency_contact_name = forms.CharField(
        max_length=100,
    )
    emergency_contact_phone = forms.CharField(
        max_length=15,
    )
    has_donated_before = forms.BooleanField()

    # class Meta:
    #     model = User
    #     fields = [
    #         "national_id",
    #         "firstname",
    #         "lastname",
    #         "gender",
    #         "age",
    #         "date_of_birth",
    #         "address",
    #         "blood_group",
    #         "emergency_contact_name",
    #         "emergency_contact_number",
    #         "number",
    #         "country",
    #     ]


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={"autofocus": True}))


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(max_length=254)


class userUpdateForm(forms.ModelForm):
    fullname = forms.CharField(max_length=50)
    number = forms.CharField(max_length=10)
    country = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ["fullname", "number", "country"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]
