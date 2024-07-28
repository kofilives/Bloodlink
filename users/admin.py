from django.contrib import admin
from .models import HospitalUser,Profile,CustomUser,Appointment

class CustomUserAdmin(admin.ModelAdmin):
  list_display = ("email", "fullname","country", "is_staff", "is_verified")
admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Profile)

admin.site.register(Appointment)

admin.site.register(HospitalUser)




