# hospitals/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from users.models import CustomUser




class HospitalAuthenticationForm(AuthenticationForm):
    username = forms.EmailInput()
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)
    
  
class HospitalAdminCreationForm(UserCreationForm):
    email= forms.EmailField(required=True)
    hospital_name= forms.CharField(max_length=255, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('hospital_name', 'email', 'password1', 'password2')
        

# class PatientInformation(forms.ModelForm):
#     national_id = forms.CharField(max_length=14)
#     firstname = forms.CharField(max_length=50)
#     lastname = forms.CharField(max_length=50)
#     gender = forms.CharField(max_length=50)
#     age = forms.IntegerField()
#     birth_date = forms.DateField()
#     address = forms.CharField(max_length=50)
#     nationality = forms.CharField()
#     email= forms.EmailField()
#     number= forms.IntegerField()
#     blood_group= forms.CharField()
#     donated_blood_before = forms.BooleanField()
#     emergency_contact_name = forms.CharField()
#     emergency_contact_number = forms.IntegerField()
    
    
    
# class PatientInfoForm(forms.ModelForm):
#     class Meta:
#         model = PatientInfo
#         fields = [
#             'ghana_card_id', 'first_name', 'last_name', 'gender', 'age', 'date_of_birth',
#             'address', 'nationality', 'email', 'phone_number', 'date', 'time', 'blood_group',
#             'has_donated_before', 'emergency_contact_name', 'emergency_contact_phone', 'terms_agreed'
#         ]
        
        
        