from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Lab Info', {'fields': ('role', 'phone', 'license_number')}),
    )
    list_display = ['username', 'email', 'role', 'is_staff']
