from django.contrib import admin
from easy_select2 import select2_modelform

# Register your models here.
from .models import Members


@admin.register(Members)
class MembersAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "is_agent", "is_customer")
    list_filter = ("first_name", "last_name", "email", "is_agent", "is_customer")
    search_fields = ("email",)
    select2 = select2_modelform(Members, attrs={"width": "250px"})
    form = select2
