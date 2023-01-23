from rest_framework import serializers
from .models import Ticket, Department, Room, Assignee


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "ticket_no",
            "department",
            "room",
            "message",
            "maintenance",
            "created_at",
            "created_by",
            "creator_name",
            "agents_assigned",
            "status",
        )


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "name")


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "room_no", "floor", "room_type", "items")


class AssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignee
        fields = ("id", "agent", "status", "is_assigned", "assigned_at")
