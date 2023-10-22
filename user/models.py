import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class AdminManagement(AbstractUser):
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
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=ROLE_USER_MANAGER)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subordinates')
    groups = models.ManyToManyField(
        Group,
        related_name='admin_users',
        blank=True,
        help_text="The groups this user belongs to.",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='admin_users_permissions',
        blank=True,
        help_text="Specific permissions for this user.",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)


class BaseTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
