from user.models import AdminManagement
from django.contrib import admin


@admin.register(AdminManagement)
class AdminManagementAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'role')
    list_filter = ('role',)
    search_fields = ('email', 'phone_number')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('phone_number', 'role')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone_number', 'role')}
         ),
    )

    filter_horizontal = ()
    list_filter = ()
