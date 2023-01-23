from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.
from .managers import MemberManager


class Members(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    room_no = models.ForeignKey(
        "buildings.Room", on_delete=models.CASCADE, null=True, blank=True
    )

    department = models.ManyToManyField(
        "buildings.Department",
        related_name="departments_assigned",
        blank=True,
        null=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = MemberManager()

    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def is_admin(self):
        return self.admin

    def __str__(self):
        return self.email
