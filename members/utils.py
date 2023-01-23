# import datetime
from buildings.models import (
    Ticket,
    Maintenance,
    Department,
    Activity,
    Building,
    Item,
    ItemSwap,
)
import datetime
import numpy as np


def get_ip_address(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def ticketData():
    x = Ticket.objects.all()
    departments = Department.objects.all().values_list("name", flat=True)
    dates = []
    data = {}
    chartdata = []
    for ticket in x:
        dates.append(ticket.created_at.strftime("%d/%m/%Y"))
        print(ticket.room.floor.block.building.name)
    dates = set(dates)
    dates = list(dates)
    print(dates)
    for i in dates:
        chartdata = []
        day, month, year = i.split("/")
        day_data = x.filter(
            created_at__day=day, created_at__month=month, created_at__year=year
        )
        for j in departments:
            chartdata.append(len(day_data.filter(department__name=j).values()))
        data[i] = {
            "labels": departments,
            "chartdata": chartdata,
        }
    return data


def tableData():
    activities = Activity.objects.all()
    tickets = Ticket.objects.all()
    departments = Department.objects.all().values_list("name", flat=True)
    row_data = {}

    table_date_data = {}
    dates = []
    for ticket in tickets:
        dates.append(ticket.created_at.strftime("%d/%m/%Y"))
    dates = set(dates)
    for date in dates:
        day, month, year = date.split("/")
        filter_ticket = tickets.filter(
            created_at__day=day, created_at__month=month, created_at__year=year
        )
        table_data = []
        # day, month, year = date.strftime("%d/%m/%Y").split("/")
        activity_filtered = activities.filter(
            closed_at__day=day, closed_at__month=month, closed_at__year=year
        )
        for i in departments:
            filter_ticket_dep = filter_ticket.filter(department__name=i)
            service_time = 0
            response_time = 0
            item_data = activity_filtered.filter(
                itemswap__items__department__name=i
            ).values_list("itemswap__items__price", flat=True)
            for j in filter_ticket:
                created_at = j.created_at
                ticket_id = j.id
                assigned_at = j.agents_assigned.filter(department__name=i).values_list(
                    "assigned_at", flat=True
                )
                closed_at = activities.filter(ticket_id=ticket_id).values_list(
                    "closed_at", flat=True
                )
                if assigned_at:
                    assigned_at_time = assigned_at[0]
                    service_time += (assigned_at_time - created_at).total_seconds() / 60
                if closed_at and assigned_at:
                    closed_at = closed_at[0]
                    assigned_at = assigned_at[0]
                    response_time += (closed_at - assigned_at).total_seconds() / 60
                else:
                    response_time += 0
            row_data = {}
            row_data["department"] = i
            row_data["opened"] = len(
                filter_ticket_dep.filter(department__name=i).values()
            )
            row_data["closed"] = len(
                filter_ticket_dep.filter(
                    department__name=i, status="Completed"
                ).values()
            )
            row_data["ServiceTime"] = service_time
            row_data["price"] = sum(item_data)
            row_data["ResponseTime"] = response_time
            table_data.append(row_data)
        table_date_data[date] = table_data

    return table_date_data


def buildingWiseData():
    activities = Activity.objects.all()
    buildings = Building.objects.all()
    departments = Department.objects.all().values_list("name", flat=True)
    departments = set(departments)
    tickets = Ticket.objects.all()
    print(tickets)
    dates = []
    data = {}
    items = Item.objects.all()  # to be used afterwards
    item_count = {}

    for ticket in tickets:
        dates.append(ticket.created_at.strftime("%d/%m/%Y"))

    dates = set(dates)
    print(dates)
    for date in dates:

        # day, month, year = date.strftime("%d/%m/%Y").split("/")
        day, month, year = date.split("/")
        tickets_filtered = tickets.filter(
            created_at__day=day, created_at__month=month, created_at__year=year
        )
        activities_filtered = activities.filter(
            closed_at__day=day, closed_at__month=month, closed_at__year=year
        )

        for building in buildings:
            building_data = {}
            table_data = []
            for department in departments:
                service_time = 0
                response_time = 0
                for j in tickets_filtered:
                    created_at = j.created_at
                    ticket_id = j.id
                    assigned_at = j.agents_assigned.filter(
                        department__name=department
                    ).values_list("assigned_at", flat=True)
                    closed_at = activities.filter(ticket_id=ticket_id).values_list(
                        "closed_at", flat=True
                    )
                    if assigned_at:
                        assigned_at_time = assigned_at[0]
                        service_time += (
                            assigned_at_time - created_at
                        ).total_seconds() / 60
                    if closed_at and assigned_at:
                        closed_at = closed_at[0]
                        assigned_at = assigned_at[0]
                        response_time += (closed_at - assigned_at).total_seconds() / 60
                    else:
                        response_time += 0
                # item_data = activities_filtered.filter(itemswap__items__department__name=department).values_list("itemswap__items__price", flat=True)
                item_names = activities_filtered.filter(
                    itemswap__items__department__name=department
                ).values_list("itemswap__items__item_name", flat=True)
                item_price = activities_filtered.filter(
                    itemswap__items__department__name=department
                ).values_list("itemswap__items__price", flat=True)
                item_count = activities_filtered.filter(
                    itemswap__items__department__name=department
                ).values_list("itemswap__count", flat=True)
                # building_data[department] = len(tickets_filtered.filter(room__floor__block__building=building, department__name=department).values())
                row_data = {}
                row_data["department"] = department
                row_data["opened"] = len(
                    tickets_filtered.filter(room__floor__block__building=building)
                    .filter(department__name=department)
                    .values()
                )
                row_data["closed"] = len(
                    tickets_filtered.filter(room__floor__block__building=building)
                    .filter(department__name=department, status="Completed")
                    .values()
                )
                row_data["ServiceTime"] = service_time
                row_data["ResponseTime"] = response_time
                # row_data["building"] = building.name
                item_data = np.multiply(item_price, item_count)
                row_data["price"] = item_data
                row_data["items"] = item_names
                table_data.append(row_data)
            # building_data['building'] = building.name
            building_data[building.name] = table_data
        data[date] = building_data
        data["buildings"] = buildings.values_list("name", flat=True)
    # return activities.filter(itemswap__items__department__name="Electrical").values()
    return data


def departmentPrice():
    departments = Department.objects.all()
    dates = []

    data = {}
    activities = Activity.objects.all()
    for activity in activities:
        dates.append(activity.closed_at)
    dates = set(dates)
    dates = list(dates)
    for date in dates:
        table_data = []
        day, month, year = date.strftime("%d/%m/%Y").split("/")
        activities_filtered = activities.filter(
            closed_at__day=day, closed_at__month=month, closed_at__year=year
        )
        for department in departments:
            row_data = {}
            item_names = activities_filtered.filter(
                itemswap__items__department__name=department
            ).values_list("itemswap__items__item_name", flat=True)
            item_price = activities_filtered.filter(
                itemswap__items__department__name=department
            ).values_list("itemswap__items__price", flat=True)
            item_count = activities_filtered.filter(
                itemswap__items__department__name=department
            ).values_list("itemswap__count", flat=True)
            item_data = np.multiply(item_price, item_count)
            item_dict = {}
            print(item_names, item_data)
            item_dict = dict(zip(item_names, item_data))
            # for i in range(len(item_names)):

            # print(item_data)
            # item_data = np.multiply(item_, item_count)
            row_data["department"] = department.name
            row_data["price"] = sum(item_data)
            row_data["items"] = item_dict
            # row_data[department.name] = sum(item_data)
            table_data.append(row_data)
        data[date.strftime("%d/%m/%Y")] = table_data
    # return activities.filter(itemswap__items__department__name="Electrical").values_list("itemswap__items__item_name", flat=True)
    return data


def itemWisedata():
    activities = Activity.objects.all()
    tickets = Ticket.objects.all()
    dates = []
    data = []
    for activity in activities:
        dates.append(activity.closed_at.strftime("%d/%m/%Y"))

    dates = set(dates)
    # for date in dates:

    #     table_data = []
    #     day, month, year = date.split("/")
    #     activities_filtered = activities.filter(closed_at__day=day, closed_at__month=month, closed_at__year=year)
    #     item_count = activities_filtered.values_list("itemswap__count", flat=True)
    #     item_names = activities_filtered.values_list("itemswap__items__item_name", flat=True)
    #     item_data = {}
    #     for i in range(len(item_names)):
    #         if item_names[i] in item_data:
    #             item_data[item_names[i]] += item_count[i]
    #         else:
    #             item_data[item_names[i]] = item_count[i]
    #         # item_data[item_names[i]] = item_count[i]
    #     # row_data = {}
    #     # row_data["item"] = "Electrical"
    #     # row_data["price"] = sum(item_data)
    #     # table_data.append(row_data)
    #     data[date] = item_data

    for ticket in tickets:
        assigned_time = ticket.agents_assigned.filter(
            department__name="Electrical"
        ).values_list("assigned_at", flat=True)[0]
        created_time = ticket.created_at
        time = (assigned_time - created_time).total_seconds() / 60
        data.append(time)
    return data
