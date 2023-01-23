from django.db import models
from members.models import Members

# Create your models here.


class UserLog(models.Model):
    user = models.ForeignKey(Members, on_delete=models.CASCADE, editable=False)
    token = models.CharField(max_length=100, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ipAddress = models.GenericIPAddressField(editable=False)
    log_type = models.CharField(max_length=100, editable=False)

    class Meta:
        verbose_name_plural = "User Logs"
