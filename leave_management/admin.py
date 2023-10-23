from django.contrib import admin
from .models import LeaveType, LeaveApplication, RestrictedDays, LeavePolicy


# Register the LeaveType model
@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('leave_type_name', 'days_allowed_in_a_year', 'days_allowed_in_a_month')


# Register the LeaveApplication model
@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'leave_status', 'start_date', 'end_date', 'leave_type', 'manager')
    list_filter = ('leave_status', 'leave_type', 'manager')
    search_fields = ('employee_name', 'employee_id')


# Register the RestrictedDays model
@admin.register(RestrictedDays)
class RestrictedDaysAdmin(admin.ModelAdmin):
    list_display = ('day_name', 'date')
    list_filter = ('day_name',)
    search_fields = ('day_name',)


# Register the LeavePolicy model
@admin.register(LeavePolicy)
class LeavePolicyAdmin(admin.ModelAdmin):
    list_display = ('leave_taken', 'restricted_days', 'paid_leave_per_year')
