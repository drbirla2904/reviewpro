from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email','full_name','plan','is_active','created_at']
    list_filter = ['plan','is_active']
    search_fields = ['email','full_name']
    ordering = ['-created_at']
    fieldsets = UserAdmin.fieldsets + (('ReviewPro', {'fields': ('full_name','plan','avatar_initials','email_verified','onboarding_done')}),)
