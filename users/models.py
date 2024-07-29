# from .fields import EncryptedTextField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    def _create_user(
        self,
        email,
        password=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_verified", False)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def update_user(
        self,
        national_id,
        firstname,
        lastname,
        gender,
        age,
        date_of_birth,
        address,
        blood_group,
        emergency_contact_name,
        emergency_contact_number,
        number,
        country,
    ):
        if not firstname:
            raise ValueError("The Firstname field must be set")
        user = self.model(
            firstname=firstname,
            number=number,
            country=country,
            national_id=national_id,
            lastname=lastname,
            gender=gender,
            age=age,
            date_of_birth=date_of_birth,
            address=address,
            blood_group=blood_group,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_number=emergency_contact_number,
            
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    role= models.CharField(max_length=15, null=True)
    national_id = models.CharField(max_length=15,null=True, blank= True, unique=True)
    fullname = models.CharField(max_length=50, null=True, blank= True)
    first_name = models.CharField(max_length=100, null=True, blank= True)
    last_name = models.CharField(max_length=100, null=True, blank= True)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=50, null=True, blank= True)
    gender = models.CharField(max_length=10,null=True, blank= True)
    age = models.IntegerField(null=True, blank= True)
    joined_date = models.DateField(null=True, blank= True)
    date_of_birth = models.DateField(null=True, blank= True)
    address = models.CharField(max_length=255,null=True, blank= True)
    nationality = models.CharField(max_length=100,null=True, blank= True)
    phone_number = models.CharField(max_length=15,null=True, blank= True)
    blood_group = models.CharField(max_length=30,null=True, blank= True)
    appointment_date=models.DateField(null=True, blank= True)
    appointment_time= models.TimeField(null=True, blank= True)
    
    
    emergency_contact_name = models.CharField(max_length=100,null=True, blank= True)
    emergency_contact_phone = models.CharField(max_length=15,null=True, blank= True)
    has_donated_before = models.BooleanField(null=True, blank= True)
    terms_agreed = models.BooleanField(default=False,null=True, blank= True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    hospital_users = models.ManyToManyField('HospitalUser', related_name='custom_users',blank=True)
    bloods = models.ManyToManyField('Blood', related_name='custom_users',blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # changed related_name to customuser_set
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # changed related_name to customuser_set
        blank=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} {self.fullname}"




class HospitalUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=50, null=True, blank= True)
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    
    bloods = models.ManyToManyField('Blood', related_name='hospital_users', blank=True)

    def __str__(self):
        return f"Name of Hospital: {self.user.fullname}"


class Blood(models.Model):
    blood_type = models.CharField(max_length=8, blank=True,null=True)

    def __str__(self):
        return self.blood_type

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.email} Profile Picture"


class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, null=True)
    date = models.DateField()
    time = models.TimeField()
    has_donated_before = models.BooleanField()
    terms_agreed = models.BooleanField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.date} {self.time}"

