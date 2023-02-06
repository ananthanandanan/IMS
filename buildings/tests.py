from django.test import TestCase

# Create your tests here.

from .models import *
from datetime import date
import datetime
from members.models import Members
from django.utils import timezone


class DepartmentTestCase(TestCase):
    def setUp(self):
        Department.objects.create(name="IT Dept", id=1)

    def test_department(self):
        dep = Department.objects.get(id=1)
        self.assertEqual(dep.name, "IT Dept")


class BuildingTestCase(TestCase):
    def setUp(self):
        Building.objects.create(name="Building 1", id=1)

    def test_building(self):
        b1 = Building.objects.get(id=1)
        self.assertEqual(b1.name, "Building 1")


class BlockTestCase(TestCase):
    def setUp(self):
        Building.objects.create(name="Building 1", id=1)
        Block.objects.create(
            name="Block 1", id=1, building=Building.objects.get(id=1), floors=5
        )

    def test_block(self):
        b1 = Block.objects.get(id=1)
        self.assertEqual(b1.name, "Block 1")
        self.assertEqual(b1.floors, 5)


class FloorTestCase(TestCase):
    def setUp(self):
        Building.objects.create(name="Building 1", id=1)
        Block.objects.create(
            name="Block 1", id=1, building=Building.objects.get(id=1), floors=5
        )
        Floor.objects.create(
            name="Floor 1", id=1, block=Block.objects.get(id=1), no_rooms=10
        )

    def test_floor(self):
        f1 = Floor.objects.get(id=1)
        self.assertEqual(f1.name, "Floor 1")
        self.assertEqual(f1.block.name, "Block 1")
        self.assertEqual(f1.no_rooms, 10)


class ItemTestCase(TestCase):
    def setUp(self):
        Department.objects.create(name="IT Dept", id=1)
        Item.objects.create(
            item_name="Item 1",
            id=1,
            department=Department.objects.get(id=1),
            item_type="Bulb",
            item_value="200W",
            price=1000,
        )

    def test_item(self):
        i1 = Item.objects.get(id=1)
        self.assertEqual(i1.item_name, "Item 1")
        self.assertEqual(i1.department.name, "IT Dept")
        self.assertEqual(i1.item_type, "Bulb")
        self.assertEqual(i1.item_value, "200W")
        self.assertEqual(i1.price, 1000)


class RoomTypeTestCase(TestCase):
    def setUp(self):
        RoomType.objects.create(name="Room Type 1", id=1)

    def test_room_type(self):
        rt1 = RoomType.objects.get(id=1)
        self.assertEqual(rt1.name, "Room Type 1")


class RoomTestCase(TestCase):
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

    def test_room(self):
        r1 = Room.objects.get(id=1)
        self.assertEqual(r1.room_no, 1)
        self.assertEqual(r1.floor.name, "Floor 1")
        self.assertEqual(r1.room_type.name, "Room Type 1")
        self.assertEqual(r1.items.first().item_name, "Item 1")


class RoomItemTestCase(TestCase):
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
        RoomItem.objects.create(
            room=Room.objects.get(id=1), item=Item.objects.get(id=1), count=10
        )

    def test_room_item(self):
        ri1 = RoomItem.objects.get(room=Room.objects.get(id=1))
        self.assertEqual(ri1.room.room_no, 1)
        self.assertEqual(ri1.item.item_name, "Item 1")
        self.assertEqual(ri1.count, 10)


class MaintenanceTestCase(TestCase):
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
        )
        Maintenance.objects.create(
            id=1,
            maintenance_type="Daily",
            maintenance_name="Change Bulb",
            maintenance_date=date.today(),
            maintenance_description="Change Bulb",
            admin=Members.objects.get(id=1),
        )
        main = Maintenance.objects.get(id=1)
        main.departments.add(Department.objects.get(id=1))
        main.rooms.add(Room.objects.get(id=1))

    def test_maintenance(self):
        m1 = Maintenance.objects.get(rooms=Room.objects.get(id=1))
        self.assertEqual(m1.maintenance_type, "Daily")
        self.assertEqual(m1.maintenance_name, "Change Bulb")
        self.assertEqual(m1.maintenance_date, date.today())
        self.assertEqual(m1.maintenance_description, "Change Bulb")
        self.assertEqual(m1.rooms.first().room_no, 1)
        self.assertEqual(m1.departments.first().name, "IT Dept")


class AssigneeTestCase(TestCase):

    # global timestamp
    # timestamp = datetime.now()

    def setUp(self):
        # set agent
        Members.objects.create(
            id=1,
            email="agent@gmail.com",
            first_name="Agent",
            last_name="Agent",
            is_active=True,
            is_staff=True,
            is_agent=True,
            is_customer=False,
            admin=False,
        )
        self.now = timezone.now()
        # create Assignee
        Assignee.objects.create(
            id=1,
            agent=Members.objects.get(id=1),
            is_assigned=False,
            assigned_at=self.now,
            status="Pending",
        )

    def test_assignee(self):
        a1 = Assignee.objects.get(id=1)
        self.assertEqual(a1.agent.first_name, "Agent")
        self.assertEqual(a1.agent.last_name, "Agent")
        self.assertEqual(a1.is_assigned, False)

        # allow for 2ms difference
        time_difference = datetime.timedelta(seconds=2)
        self.assertAlmostEqual(a1.assigned_at, self.now, delta=time_difference)
        self.assertEqual(a1.status, "Pending")


class TicketTestCase(TestCase):
    def setUp(self):
        # set customer
        Members.objects.create(
            id=1,
            email="customer@gmail.com",
            first_name="Customer",
            last_name="Customer",
            is_active=True,
            is_staff=False,
            is_agent=False,
            is_customer=True,
            admin=False,
        )

        # set agent
        Members.objects.create(
            id=2,
            email="agent@gmail.com",
            first_name="Agent",
            last_name="Agent",
            is_active=True,
            is_staff=True,
            is_agent=True,
            is_customer=False,
            admin=False,
        )

        # set room
        Building.objects.create(name="Building 1", id=1)
        Block.objects.create(
            name="Block 1", id=1, building=Building.objects.get(id=1), floors=5
        )
        Floor.objects.create(
            name="Floor 1", id=1, block=Block.objects.get(id=1), no_rooms=10
        )
        RoomType.objects.create(name="Room Type 1", id=1)
        Room.objects.create(
            id=1,
            room_no=1,
            floor=Floor.objects.get(id=1),
            room_type=RoomType.objects.get(id=1),
        )

        # set department
        Department.objects.create(name="IT Dept", id=1)

        # set Assignee
        Assignee.objects.create(
            id=1,
            agent=Members.objects.get(id=2),
            is_assigned=True,
            assigned_at=timezone.now(),
            status="Pending",
        )

        # set maintenance

        Maintenance.objects.create(
            id=1,
            maintenance_type="Daily",
            maintenance_name="Change Bulb",
            maintenance_date=date.today(),
            maintenance_description="Change Bulb",
            admin=Members.objects.get(id=1),
        )
        global ticket_no
        ticket_no = uuid.uuid4()
        Ticket.objects.create(
            id=1,
            ticket_no=ticket_no,
            creator_name=Members.objects.get(id=1).first_name,
            room=Room.objects.get(id=1),
            message="Change Bulb",
            maintenance=Maintenance.objects.get(id=1),
            created_at=timezone.now(),
            created_by=Members.objects.get(id=1),
            status="Pending",
        )
        Ticket.objects.get(id=1).department.add(Department.objects.get(id=1))
        Ticket.objects.get(id=1).agents_assigned.add(Assignee.objects.get(id=1))

    def test_ticket(self):
        t1 = Ticket.objects.get(id=1)
        self.assertEqual(t1.ticket_no, ticket_no)
        self.assertEqual(t1.creator_name, "Customer")
        self.assertEqual(t1.department.first().name, "IT Dept")
        self.assertEqual(t1.room.room_no, 1)
        self.assertEqual(t1.message, "Change Bulb")
        self.assertEqual(t1.maintenance.maintenance_name, "Change Bulb")
        self.assertEqual(t1.created_by.first_name, "Customer")
        self.assertEqual(t1.agents_assigned.first().agent.first_name, "Agent")
        self.assertEqual(t1.status, "Pending")


class AcitivityTestCase(TestCase):
    def setUp(self):
        # set customer
        Members.objects.create(
            id=1,
            email="customer@gmail.com",
            first_name="Customer",
            last_name="Customer",
            is_active=True,
            is_staff=False,
            is_agent=False,
            is_customer=True,
            admin=False,
        )

        # set agent
        Members.objects.create(
            id=2,
            email="agent@gmail.com",
            first_name="Agent",
            last_name="Agent",
            is_active=True,
            is_staff=True,
            is_agent=True,
            is_customer=False,
            admin=False,
        )

        # set room
        Building.objects.create(name="Building 1", id=1)
        Block.objects.create(
            name="Block 1", id=1, building=Building.objects.get(id=1), floors=5
        )
        Floor.objects.create(
            name="Floor 1", id=1, block=Block.objects.get(id=1), no_rooms=10
        )
        RoomType.objects.create(name="Room Type 1", id=1)
        Room.objects.create(
            id=1,
            room_no=1,
            floor=Floor.objects.get(id=1),
            room_type=RoomType.objects.get(id=1),
        )

        # set department
        Department.objects.create(name="IT Dept", id=1)

        # set Assignee
        Assignee.objects.create(
            id=1,
            agent=Members.objects.get(id=2),
            is_assigned=True,
            assigned_at=timezone.now(),
            status="Pending",
        )

        # set maintenance

        Maintenance.objects.create(
            id=1,
            maintenance_type="Daily",
            maintenance_name="Change Bulb",
            maintenance_date=date.today(),
            maintenance_description="Change Bulb",
            admin=Members.objects.get(id=1),
        )
        global ticket_no
        ticket_no = uuid.uuid4()
        Ticket.objects.create(
            id=1,
            ticket_no=ticket_no,
            creator_name=Members.objects.get(id=1).first_name,
            room=Room.objects.get(id=1),
            message="Change Bulb",
            maintenance=Maintenance.objects.get(id=1),
            created_at=timezone.now(),
            created_by=Members.objects.get(id=1),
            status="Pending",
        )
        Ticket.objects.get(id=1).department.add(Department.objects.get(id=1))
        Ticket.objects.get(id=1).agents_assigned.add(Assignee.objects.get(id=1))

        Activity.objects.create(
            id=1,
            ticket=Ticket.objects.get(id=1),
            comments="Bulb Changed",
            closed_at=timezone.now(),
        )

    def test_activity(self):
        a1 = Activity.objects.get(id=1)
        self.assertEqual(a1.ticket.ticket_no, ticket_no)
        self.assertEqual(a1.comments, "Bulb Changed")
        time_difference = datetime.timedelta(seconds=2)
        self.assertAlmostEqual(a1.closed_at, timezone.now(), delta=time_difference)


class ItemSwapTestCase(TestCase):
    def setUp(self):
        Members.objects.create(
            id=1,
            email="customer@gmail.com",
            first_name="Customer",
            last_name="Customer",
            is_active=True,
            is_staff=False,
            is_agent=False,
            is_customer=True,
            admin=False,
        )

        # set agent
        Members.objects.create(
            id=2,
            email="agent@gmail.com",
            first_name="Agent",
            last_name="Agent",
            is_active=True,
            is_staff=True,
            is_agent=True,
            is_customer=False,
            admin=False,
        )

        # set room
        Building.objects.create(name="Building 1", id=1)
        Block.objects.create(
            name="Block 1", id=1, building=Building.objects.get(id=1), floors=5
        )
        Floor.objects.create(
            name="Floor 1", id=1, block=Block.objects.get(id=1), no_rooms=10
        )
        RoomType.objects.create(name="Room Type 1", id=1)
        Room.objects.create(
            id=1,
            room_no=1,
            floor=Floor.objects.get(id=1),
            room_type=RoomType.objects.get(id=1),
        )
        # set Items

        # set department
        Department.objects.create(name="IT Dept", id=1)

        Item.objects.create(
            item_name="Item 1",
            id=1,
            department=Department.objects.get(id=1),
            item_type="Bulb",
            item_value="200W",
            price=1000,
        )
        # set Assignee
        Assignee.objects.create(
            id=1,
            agent=Members.objects.get(id=2),
            is_assigned=True,
            assigned_at=timezone.now(),
            status="Pending",
        )

        # set maintenance

        Maintenance.objects.create(
            id=1,
            maintenance_type="Daily",
            maintenance_name="Change Bulb",
            maintenance_date=date.today(),
            maintenance_description="Change Bulb",
            admin=Members.objects.get(id=1),
        )
        global ticket_no
        ticket_no = uuid.uuid4()
        Ticket.objects.create(
            id=1,
            ticket_no=ticket_no,
            creator_name=Members.objects.get(id=1).first_name,
            room=Room.objects.get(id=1),
            message="Change Bulb",
            maintenance=Maintenance.objects.get(id=1),
            created_at=timezone.now(),
            created_by=Members.objects.get(id=1),
            status="Pending",
        )
        Ticket.objects.get(id=1).department.add(Department.objects.get(id=1))
        Ticket.objects.get(id=1).agents_assigned.add(Assignee.objects.get(id=1))

        Activity.objects.create(
            id=1,
            ticket=Ticket.objects.get(id=1),
            comments="Bulb Changed",
            closed_at=timezone.now(),
        )

        ItemSwap.objects.create(
            id=1,
            activity=Activity.objects.get(id=1),
            items=Item.objects.get(id=1),
            count=1,
        )

    def test_item_swap(self):
        a1 = ItemSwap.objects.get(id=1)
        self.assertEqual(a1.activity.ticket.ticket_no, ticket_no)
        self.assertEqual(a1.items.item_name, "Item 1")
        self.assertEqual(a1.count, 1)
