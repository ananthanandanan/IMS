from django.test import TestCase
from .models import *
from buildings.models import *

# Create your tests here.
class MembersTestCase(TestCase):
    def setUp(self):
        Building.objects.create(name="Building 1", id=1)
        Block.objects.create(
            name="Block 1", id=1, building=Building.objects.get(id=1), floors=5
        )
        Floor.objects.create(
            name="Floor 1", id=1, block=Block.objects.get(id=1), no_rooms=10
        )
        RoomType.objects.create(name="Room Type 1", id=1)
        Department.objects.create(name="IT Dept", id=1)
        Item.objects.create(
            item_name="Item 1",
            id=1,
            department=Department.objects.get(id=1),
            item_type="Bulb",
            item_value="200W",
            price=1000,
        )
        Room.objects.create(
            room_no=1,
            id=1,
            floor=Floor.objects.get(id=1),
            room_type=RoomType.objects.get(id=1),
        )
        Room.objects.get(id=1).items.add(Item.objects.get(id=1))

        Members.objects.create(
            id=1,
            email="test@gmail.com",
            first_name="Admin",
            last_name="Admin",
            is_active=True,
            is_staff=True,
            is_agent=False,
            is_customer=False,
            admin=True,
            room_no=Room.objects.get(id=1),
        )

    def test_members(self):
        m1 = Members.objects.get(id=1)
        self.assertEqual(m1.email, "test@gmail.com")
        self.assertEqual(m1.first_name, "Admin")
        self.assertEqual(m1.last_name, "Admin")
        self.assertEqual(m1.is_active, True)
        self.assertEqual(m1.is_staff, True)
        self.assertEqual(m1.is_agent, False)
        self.assertEqual(m1.is_customer, False)
        self.assertEqual(m1.admin, True)
