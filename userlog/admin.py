from django.contrib import admin

# Register your models here.
from .models import UserLog


@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ("user", "ipAddress", "log_type")
    list_filter = ("user", "created_at", "log_type")
    search_fields = ("user__email", "ipAddress")

    def has_delete_permission(self, request, obj=None):
        return False
