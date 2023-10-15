import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_SUPER_ADMIN = "SUPER_ADMIN"
    ROLE_ADMIN = "ADMIN"
    ROLE_DEFAULT_MANAGER = "DEFAULT_MANAGER"
    ROLE_USER_MANAGER = "USER_MANAGER"

    ROLE_CHOICES = (
        (ROLE_SUPER_ADMIN, 'SUPER_ADMIN'),
        (ROLE_ADMIN, "ADMIN"),
        (ROLE_DEFAULT_MANAGER, "DEFAULT_MANAGER"),
        (ROLE_USER_MANAGER, "USER_MANAGER")
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=48, null=True, blank=True)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default='')
    full_name = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.email)


class BaseTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
