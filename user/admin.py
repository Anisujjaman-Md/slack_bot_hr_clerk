from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register the User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'manager')
    list_filter = ('role',)
    search_fields = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Manager', {'fields': ('manager',)}),
        ('Role', {'fields': ('role',)}),
    )
