from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User 
from .models import customUser



# class userLoginForm(forms.ModelForm):
#     prn=forms.CharField(max_length=10)
#     password=forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model =User
#         fields= ['prn', 'password']

# class userRegistrationForm(UserCreationForm):
   

#     title = forms.ChoiceField(choices='Male' 'Female' 'Others')
#     firstname = forms.CharField(max_length=20)
#     lastname = forms.CharField(max_length=20)
#     age = forms.IntegerField(min_value=1)
#     digitalAddress = forms.CharField(max_length=20)
#     country = forms.ChoiceField(choices= 'Ghana' 'Togo' 'Others')
#     number = forms.CharField(max_length=20)
#     email = forms.EmailField()

#     class Meta:
#         model = customUser
#         fields = ['firstname', 'lastname', 'age', 'digitalAddress', 'country', 'number', 'email']






# class UserRegistrationForm(UserCreationForm):

#     date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

#     class Meta:
#         model = customUser
#         fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'username', 'password1', 'password2'] 

