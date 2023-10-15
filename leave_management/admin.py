from django.contrib import admin

from leave_management.models import LeaveApplication, LeavePolicy, RestrictedDays


@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'duration_type')
    list_filter = ('leave_type', 'duration_type')
    search_fields = ('employee__username', 'employee__first_name', 'employee__last_name', 'start_date', 'end_date')


@admin.register(LeavePolicy)
class LeavePolicyAdmin(admin.ModelAdmin):
    list_display = ('paid_leave_per_year', 'unpaid_leave_cost_per_day', 'paid_leave_taken', 'unpaid_leave_taken',
                    'leave_for_all_employees', 'max_leaves_per_month')
    list_filter = ('leave_for_all_employees',)
    search_fields = ('paid_leave_per_year', 'max_leaves_per_month')


@admin.register(RestrictedDays)
class RestrictedDaysAdmin(admin.ModelAdmin):
    list_display = ('day_name', 'date',)
