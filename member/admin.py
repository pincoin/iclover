from django.contrib import admin

from .models import (
    Profile, LoginLog, PhoneVerificationLog, Employees
)


class ProfileAdmin(admin.ModelAdmin):
    pass


class LoginLogAdmin(admin.ModelAdmin):
    pass


class PhoneVerificationLogAdmin(admin.ModelAdmin):
    pass

class EmployeesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)
admin.site.register(LoginLog, LoginLogAdmin)
admin.site.register(Employees, EmployeesAdmin)
admin.site.register(PhoneVerificationLog, PhoneVerificationLogAdmin)
