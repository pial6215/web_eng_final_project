from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Admin panel-e kon kon field dekhabe
    list_display = ['username', 'email', 'role', 'phone_number', 'is_staff']
    
    # Admin panel theke edit korar shomoy amader custom field gulo jate dekhay
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'phone_number', 'university_id')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)