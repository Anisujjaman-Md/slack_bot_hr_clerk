from django.db import models


class LeaveApplication(models.Model):
    VACATION = 'VACATION'
    SICK_LEAVE = 'SICK_LEAVE'
    MATERNITY_LEAVE = 'MATERNITY_LEAVE'

    LEAVE_TYPE_CHOICES = (
        (VACATION, 'VACATION'),
        (SICK_LEAVE, 'SICK_LEAVE'),
        (MATERNITY_LEAVE, 'MATERNITY_LEAVE'),
    )

    FULL_DAY = 'FULL_DAY'
    HALF_DAY = 'HALF_DAY'

    DURATION_TYPE_CHOICES = (
        (FULL_DAY, 'FULL_DAY'),
        (HALF_DAY, 'HALF_DAY'),
    )

    APPROVE = 'APPROVE'
    REJECT = 'REJECT'

    STATUS_CHOICES = (
        (APPROVE, 'APPROVE'),
        (REJECT, 'REJECT'),
    )

    employee = models.CharField(max_length=30, null=True, blank=True)
    leave_type = models.CharField(max_length=15, choices=LEAVE_TYPE_CHOICES)
    duration_type = models.CharField(max_length=10, choices=DURATION_TYPE_CHOICES)
    leave_status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    comment = models.TextField()

    def __str__(self):
        return f"{self.employee}'s Leave Application"


class RestrictedDays(models.Model):
    day_name = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return self.day_name


class LeavePolicy(models.Model):
    paid_leave_per_year = models.PositiveIntegerField()
    unpaid_leave_cost_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    paid_leave_taken = models.PositiveIntegerField(default=0)
    unpaid_leave_taken = models.PositiveIntegerField(default=0)
    leave_for_all_employees = models.BooleanField(default=False)
    max_leaves_per_month = models.PositiveIntegerField()
    restricted_days_of_week = models.ForeignKey(RestrictedDays, on_delete=models.SET_NULL,  null=True, blank=True)

    def __str__(self):
        return 'Leave Policy'
