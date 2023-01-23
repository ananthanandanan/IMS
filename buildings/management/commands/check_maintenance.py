from django.core.management.base import BaseCommand
from buildings.models import *
import datetime


class Command(BaseCommand):
    """This command is used to check for maintenance objects that are due today and create tickets for them."""

    def handle(self, *args, **options):
        ## Get all maintenance objects due today.
        try:
            maintenances = Maintenance.objects.all().filter(
                maintenance_date=datetime.date.today()
            )
            try:
                for maintenance in maintenances:
                    ## Create a ticket for each room in the maintenance object based on type.
                    if maintenance.maintenance_type == "Daily":
                        for room in maintenance.rooms.all():
                            ticketObj = Ticket.objects.create(
                                maintenance=maintenance,
                                room=room,
                                message=maintenance.maintenance_description,
                                created_by=maintenance.admin,
                            )
                            ## Add the departments to the ticket.
                            maintenance_departments = maintenance.departments.all()
                            ticketObj.department.add(*maintenance_departments)
                            ticketObj.save()
                        ## Update the maintenance date to tomorrow.
                        maintenance.maintenance_date = (
                            datetime.date.today() + datetime.timedelta(days=1)
                        )
                        maintenance.save()
                    elif maintenance.maintenance_type == "Weekly":
                        for room in maintenance.rooms.all():
                            ticketObj = Ticket.objects.create(
                                maintenance=maintenance,
                                room=room,
                                message=maintenance.maintenance_description,
                                created_by=maintenance.admin,
                            )
                            ## Add the departments to the ticket.
                            maintenance_departments = maintenance.departments.all()
                            ticketObj.department.add(*maintenance_departments)
                            ticketObj.save()
                        ## Update the maintenance date to next week.
                        maintenance.maintenance_date = (
                            datetime.date.today() + datetime.timedelta(days=7)
                        )
                        maintenance.save()
                    elif maintenance.maintenance_type == "Monthly":
                        for room in maintenance.rooms.all():
                            ticketObj = Ticket.objects.create(
                                maintenance=maintenance,
                                room=room,
                                message=maintenance.maintenance_description,
                                created_by=maintenance.admin,
                            )
                            ## Add the departments to the ticket.
                            maintenance_departments = maintenance.departments.all()
                            ticketObj.department.add(*maintenance_departments)
                            ticketObj.save()
                        ## Update the maintenance date to next month.
                        maintenance.maintenance_date = (
                            datetime.date.today() + datetime.timedelta(days=30)
                        )
                        maintenance.save()
                    elif maintenance.maintenance_type == "Quarterly":
                        for room in maintenance.rooms.all():
                            ticketObj = Ticket.objects.create(
                                maintenance=maintenance,
                                room=room,
                                message=maintenance.maintenance_description,
                                created_by=maintenance.admin,
                            )
                            ## Add the departments to the ticket.
                            maintenance_departments = maintenance.departments.all()
                            ticketObj.department.add(*maintenance_departments)
                            ticketObj.save()
                        ## Update the maintenance date to next quarter.
                        maintenance.maintenance_date = (
                            datetime.date.today() + datetime.timedelta(days=90)
                        )
                        maintenance.save()
                    elif maintenance.maintenance_type == "Half Yearly":
                        for room in maintenance.rooms.all():
                            ticketObj = Ticket.objects.create(
                                maintenance=maintenance,
                                room=room,
                                message=maintenance.maintenance_description,
                                created_by=maintenance.admin,
                            )
                            ## Add the departments to the ticket.
                            maintenance_departments = maintenance.departments.all()
                            ticketObj.department.add(*maintenance_departments)
                            ticketObj.save()
                        ## Update the maintenance date to next half year.
                        maintenance.maintenance_date = (
                            datetime.date.today() + datetime.timedelta(days=180)
                        )
                        maintenance.save()
                    else:
                        for room in maintenance.rooms.all():
                            ticketObj = Ticket.objects.create(
                                maintenance=maintenance,
                                room=room,
                                message=maintenance.maintenance_description,
                                created_by=maintenance.admin,
                            )
                            ## Add the departments to the ticket.
                            maintenance_departments = maintenance.departments.all()
                            ticketObj.department.add(*maintenance_departments)
                            ticketObj.save()
                        ## Update the maintenance date to next year.
                        maintenance.maintenance_date = (
                            datetime.date.today() + datetime.timedelta(days=365)
                        )
                        maintenance.save()
            except:
                pass
        except maintenances is None:
            pass
