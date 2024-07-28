# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# class HospitalManager(BaseUserManager):
#     def _create_hospital(self, email,hospital_name, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         hospital = self.model(email=email,hospital_name= hospital_name, **extra_fields)
#         hospital.set_password(password)
#         hospital.save(using=self._db)
#         return hospital
    
#     def create_hospital(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_active', False)
#         extra_fields.setdefault('is_verified', False)
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_hospital(email, password, **extra_fields)

#     def create_superuser(self, email,hospital_name, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_hospital(email, password,hospital_name=hospital_name **extra_fields)

# class Hospital(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     hospital_name = models.CharField(max_length=255, unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#     is_verified = models.BooleanField(default=False)

  
    
#     objects = HospitalManager()

#     USERNAME_FIELD = 'hospital_name'
#     REQUIRED_FIELDS = ['email']

#     def __str__(self):
#         return self.hospital_name
    


# class PatientInfo(models.Model):
#     ghana_card_id = models.CharField(max_length=15)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     gender = models.CharField(max_length=10)
#     age = models.IntegerField()
#     date_of_birth = models.DateField()
#     address = models.CharField(max_length=255)
#     nationality = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone_number = models.CharField(max_length=15)
#     date = models.DateField()
#     time = models.TimeField()
#     blood_group = models.CharField(max_length=3)
#     has_donated_before = models.BooleanField()
#     emergency_contact_name = models.CharField(max_length=100)
#     emergency_contact_phone = models.CharField(max_length=15)
#     terms_agreed = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"