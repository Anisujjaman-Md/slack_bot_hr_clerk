from django.db import models
from slack import WebClient
from config import settings

client = WebClient(token=settings.SLACK_TOKEN)
member_list_data = client.users_list()


class SlackUserInfo(models.Model):
    employee_id = models.CharField(max_length=255)
    team_id = models.CharField(max_length=255)
    deleted = models.BooleanField()
    real_name = models.CharField(max_length=255)
    is_admin = models.BooleanField()
    is_owner = models.BooleanField()
    is_primary_owner = models.BooleanField()
    is_restricted = models.BooleanField()
    is_ultra_restricted = models.BooleanField()
    is_bot = models.BooleanField()

    def __str__(self):
        return self.real_name

    def save(self, *args, **kwargs):
        for member_data in member_list_data['members']:
            try:
                slack_user = SlackUserInfo.objects.get(employee_id=member_data['id'])
            except SlackUserInfo.DoesNotExist:
                slack_user = SlackUserInfo(employee_id=member_data['id'])

            slack_user = SlackUserInfo(
                employee_id=member_data['id'],
                team_id=member_data['team_id'],
                deleted=member_data['deleted'],
                real_name=member_data['real_name'],
                is_admin=member_data['is_admin'],
                is_owner=member_data['is_owner'],
                is_primary_owner=member_data['is_primary_owner'],
                is_restricted=member_data['is_restricted'],
                is_ultra_restricted=member_data['is_ultra_restricted'],
                is_bot=member_data['is_bot'],
            )
            slack_user.save()
        super(SlackUserInfo, self).save(*args, **kwargs)
