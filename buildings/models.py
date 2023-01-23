from django.db import models
import uuid
from django.core.exceptions import ValidationError

# Create your models here.


class Building(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200, default="state")
    zip = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Block(models.Model):

    name = models.CharField(max_length=200, unique=True)
    floors = models.IntegerField()
    id = models.AutoField(primary_key=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{ self.building.name } <> { self.name }"


class Floor(models.Model):
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    no_rooms = models.IntegerField()
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True)

    def clean(self):
        floor_no_block = self.block.floors
        floor_count = self.block.floor_set.all().count()
        floor_exist = self.block.floor_set.filter(id=self.id).exists()

        if (not floor_exist) and (floor_no_block < floor_count + 1):
            raise ValidationError("Block Floor Limit exceeded!")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.block.building.name}<>{self.block.name}<>{ self.name }"


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=200, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    item_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Enter the item type (e.g. Fan, Tubelight Table, Chair, etc.)",
    )
    item_value = models.CharField(
        max_length=200,
        help_text="Enter item value(e.g. 40W)",
        blank=True,
        null=True,
    )
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.item_name


class RoomType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    room_no = models.IntegerField()
    id = models.AutoField(primary_key=True)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, null=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(
        Item, related_name="room_items", blank=True, through="RoomItem"
    )

    def __str__(self):
        return f"{self.floor.block.building.name}<> {self.floor.block.name} <> {self.floor.name} <> {self.room_no}"

    def clean(self):
        room_no_floor = self.floor.no_rooms
        rooms_count = self.floor.room_set.all().count()
        room_exist = self.floor.room_set.filter(id=self.id).exists()
        ## if room does not exist, then raise an error
        if (not room_exist) and (room_no_floor < rooms_count + 1):
            raise ValidationError("Floor Room Limit exceeded!")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class RoomItem(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def __str__(self):

        return f"{self.item.item_name} X {self.count}"


class Maintenance(models.Model):
    MAINTENANCE_TYPE = (
        ("Daily", "Daily"),
        ("Weekly", "Weekly"),
        ("Monthly", "Monthly"),
        ("Quarterly", "Quarterly"),
        ("Half Yearly", "Half Yearly"),
        ("Yearly", "Yearly"),
    )
    id = models.AutoField(primary_key=True)
    maintenance_name = models.CharField(max_length=200, unique=True)
    maintenance_date = models.DateField()
    maintenance_description = models.TextField()
    maintenance_type = models.CharField(
        max_length=200, choices=MAINTENANCE_TYPE, default="Daily"
    )
    departments = models.ManyToManyField(
        Department, related_name="maintenance_department"
    )
    rooms = models.ManyToManyField(Room, related_name="maintenance_rooms")
    admin = models.ForeignKey(
        "members.Members",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="created_admin",
    )

    def __str__(self):
        return self.maintenance_name


class Assignee(models.Model):
    id = models.BigAutoField(primary_key=True)
    agent = models.ForeignKey(
        "members.Members", on_delete=models.CASCADE, null=True, blank=True
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    is_assigned = models.BooleanField(default=False)
    assigned_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Completed", "Completed"),
    )
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return self.agent.email


class Ticket(models.Model):
    ticket_no = models.UUIDField(default=uuid.uuid4, editable=False)
    creator_name= models.CharField(max_length=50, blank=True, null=True)
    department = models.ManyToManyField(
        Department, related_name="ticket_department", blank=True
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    message = models.TextField()  # about the maintenance
    maintenance = models.ForeignKey(
        Maintenance, on_delete=models.CASCADE, null=True, blank=True
    )
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Completed", "Completed"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "members.Members",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="ticket_created_by",
    )

    agents_assigned = models.ManyToManyField(
        Assignee, related_name="agents_assigned", blank=True, null=True
    )

    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return str(self.ticket_no)


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    comments = models.TextField()
    closed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Activities"

    def __str__(self):
        return str(self.id) + "#" + str(self.ticket.ticket_no)


class ItemSwap(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    items = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Item Swaps"

    def __str__(self):
        return f"{self.items.item_name} X {self.count}"
