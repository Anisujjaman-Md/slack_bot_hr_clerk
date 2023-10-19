from django.db import models
from slack import WebClient
from config import settings
from datetime import datetime

client = WebClient(token=settings.SLACK_TOKEN)


class LeaveApplication(models.Model):

    FULL_DAY = 'FULL_DAY'
    HALF_DAY = 'HALF_DAY'

    DURATION_TYPE_CHOICES = (
        (FULL_DAY, 'FULL_DAY'),
        (HALF_DAY, 'HALF_DAY'),
    )

    APPROVE = 'APPROVE'
    DENY = 'DENY'

    STATUS_CHOICES = (
        (APPROVE, 'APPROVE'),
        (DENY, 'DENY'),
    )

    employee_id = models.CharField(max_length=30, null=True, blank=True)
    employee_name = models.CharField(max_length=30, null=True, blank=True)
    channel_id = models.CharField(max_length=30, null=True, blank=True)
    duration = models.PositiveIntegerField(default=0, null=True, blank=True)
    leave_status = models.CharField(max_length=7, choices=STATUS_CHOICES, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee_name}'s Leave Application"

    def calculate_duration(self):
        if self.start_date and self.end_date:
            start_date = datetime.strptime(str(self.start_date), "%Y-%m-%d")
            end_date = datetime.strptime(str(self.end_date), "%Y-%m-%d")
            delta = end_date - start_date
            self.duration = delta.days + 1
            return self.duration
        return None

    def save(self, *args, **kwargs):
        # Check if the status has changed
        self.calculate_duration()
        if self.pk:  # Check if the instance is already in the database (updating)
            old_instance = LeaveApplication.objects.get(pk=self.pk)
            if self.leave_status == LeaveApplication.APPROVE:
                client.chat_postMessage(channel=old_instance.channel_id,
                                        text=f'Hey <@{old_instance.employee_id}>, Yes! Your leave application is '
                                             f'*Approved* :smile:')
            if self.leave_status == LeaveApplication.DENY:
                client.chat_postMessage(channel=old_instance.channel_id,
                                        text=f'Hey <@{old_instance.employee_id}>, Sorry! Your leave application is '
                                             f'*Denied* :cry:')
        super(LeaveApplication, self).save(*args, **kwargs)


class RestrictedDays(models.Model):
    day_name = models.CharField(max_length=30, null=True, blank=True)
    date = models.DateField()

    def save(self, *args, **kwargs):
        self.day_name = self.date.strftime('%A')  # Set day_name based on the date field
        super(RestrictedDays, self).save(*args, **kwargs)


class LeavePolicy(models.Model):
    paid_leave_per_year = models.PositiveIntegerField()
    unpaid_leave_cost_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    paid_leave_taken = models.PositiveIntegerField(default=0)
    unpaid_leave_taken = models.PositiveIntegerField(default=0)
    leave_for_all_employees = models.BooleanField(default=False)
    max_leaves_per_month = models.PositiveIntegerField()

    def __str__(self):
        return 'Leave Policy'
