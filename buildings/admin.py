from django.contrib import admin
from easy_select2 import select2_modelform
from .inline import *

# Register your models here.
from .models import (
    Building,
    Block,
    Floor,
    Room,
    Item,
    Department,
    Maintenance,
    Ticket,
    Activity,
    RoomType,
    Assignee,
)
from django.contrib import admin


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "country")
    list_filter = ("state", "country")
    search_fields = ("name", "state", "country")


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("name", "floors")
    list_filter = ("name", "floors", "building")
    search_fields = ("name", "floors")


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ("name", "no_rooms")
    list_filter = ("name", "no_rooms", "block", "block__building")
    search_fields = ("name", "no_rooms")
    raw_id_fields = ("block",)


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Room)
class roomsAdmin(admin.ModelAdmin):
    list_display = ("room_no", "room_type", "floor")
    list_filter = (
        "room_no",
        "room_type",
        "floor",
        "floor__block",
        "floor__block__building",
    )
    raw_id_fields = ("floor",)
    search_fields = ("room_no",)
    inlines = [RoomItemInline]
    roomtype_select = select2_modelform(Room, attrs={"width": "250px"})
    form = roomtype_select


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Item)
class itemAdmin(admin.ModelAdmin):
    list_display = ("item_name", "item_type")
    list_filter = ("item_name", "item_type", "department")
    search_fields = ("item_name", "item_type")


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ("maintenance_name", "maintenance_date", "maintenance_description")
    list_filter = ("maintenance_name", "maintenance_date", "maintenance_description")
    search_fields = ("maintenance_name", "maintenance_date")
    select2 = select2_modelform(Maintenance, attrs={"width": "250px"})
    form = select2

    exclude = ("admin",)

    def save_model(self, request, obj, form, change):
        obj.admin = request.user
        obj.save()


@admin.register(Assignee)
class AssigneeAdmin(admin.ModelAdmin):
    list_display = ("agent", "is_assigned")
    list_filter = ("agent", "is_assigned")
    search_fields = ("agent__first_name", "is_assigned")
    select2 = select2_modelform(Assignee, attrs={"width": "250px"})
    form = select2


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("ticket_no", "room")
    list_filter = ("ticket_no", "room", "created_at")
    search_fields = ("ticket_no", "room")
    select2 = select2_modelform(Ticket, attrs={"width": "250px"})
    form = select2


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "comments", "closed_at")
    list_filter = ("id", "comments", "closed_at")
    search_fields = ("id", "comments", "closed_at")
    inlines = [ItemSwapInline]


@admin.register(ItemSwap)
class ItemSwapAdmin(admin.ModelAdmin):
    list_display = ("items", "count")
    list_filter = ("items__item_name", "count")
    search_fields = ("items__item_name", "count")
