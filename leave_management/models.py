from django.db import models
from user.models import User
from slack import WebClient
from config import settings
from datetime import datetime

client = WebClient(token=settings.SLACK_TOKEN)


class LeaveType(models.Model):
    leave_type_name = models.CharField(max_length=50)
    days_allowed_in_a_year = models.PositiveIntegerField(default=0)
    days_allowed_in_a_month = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.leave_type_name}"

    def save(self, *args, **kwargs):
        self.leave_type_name = self.leave_type_name.upper()
        super(LeaveType, self).save(*args, **kwargs)


class LeaveApplication(models.Model):
    PENDING = 'PENDING'
    APPROVE = 'APPROVE'
    DENY = 'DENY'

    STATUS_CHOICES = (
        (APPROVE, 'APPROVE'),
        (PENDING, 'PENDING'),
        (DENY, 'DENY'),
    )
    employee_id = models.CharField(max_length=30, null=True, blank=True)
    slack_channel = models.CharField(max_length=100, null=True, blank=True)
    employee_name = models.CharField(max_length=30, null=True, blank=True)
    channel_id = models.CharField(max_length=30, null=True, blank=True)
    duration = models.PositiveIntegerField(default=0, null=True, blank=True)
    leave_status = models.CharField(max_length=7, choices=STATUS_CHOICES, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    Leave_type = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager_leave_requests',
                                null=True)

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
    leave_taken = models.PositiveIntegerField(default=0)
    restricted_days = models.ForeignKey(RestrictedDays, on_delete=models.SET_NULL, null=True, blank=True)
    paid_leave_per_year = models.PositiveIntegerField()

    def __str__(self):
        return 'Leave Policy'
