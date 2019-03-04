from django.contrib import admin

from .models import (
    Profile, LoginLog, PhoneVerificationLog, Employees, Ask
)

class ProfileAdmin(admin.ModelAdmin):
    pass

class LoginLogAdmin(admin.ModelAdmin):
    pass

class PhoneVerificationLogAdmin(admin.ModelAdmin):
    pass

class EmployeesAdmin(admin.ModelAdmin):
    pass

class AskAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)
admin.site.register(LoginLog, LoginLogAdmin)
admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Ask, AskAdmin)
admin.site.register(PhoneVerificationLog, PhoneVerificationLogAdmin)
