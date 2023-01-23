from django.contrib import admin
from easy_select2 import select2_modelform
from .models import RoomItem, Ticket, ItemSwap

"""This file is used to create inline forms for the admin page.
This contains modules:
    RoomItemInline
    ItemSwapInline
    MaintenanceTicketInline
"""


class RoomItemInline(admin.TabularInline):
    model = RoomItem
    extra = 1


class ItemSwapInline(admin.TabularInline):
    model = ItemSwap
    extra = 1


class MaintenanceTicketInline(admin.StackedInline):
    model = Ticket
    extra = 1
