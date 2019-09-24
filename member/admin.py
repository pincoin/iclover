from django.contrib import admin

from .models import (
    Profile, LoginLog, PhoneVerificationLog, CustomerProfile
)

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['company']

class CustomerProfileAdmin(admin.ModelAdmin):
    search_fields = ['company']

class LoginLogAdmin(admin.ModelAdmin):
    pass

class PhoneVerificationLogAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(LoginLog, LoginLogAdmin)

admin.site.register(PhoneVerificationLog, PhoneVerificationLogAdmin)
