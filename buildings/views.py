from django.shortcuts import render
from django.utils import timezone
from django.views.generic.list import ListView
from buildings.models import Building
from django.contrib import admin
from members.models import Members
from .models import Ticket, Department,Room, Activity
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import *

def index(request):
    return render(request, "index.html")

@api_view(['POST'])
def postTicket(request):
    value={}
    department=[]
    department.append(int(request.data['department']))
    value['department']=department
    value['room']=int(request.data['room'])
    value['message']=request.data['message']
    value["creator_name"]=request.data['patientName']
    serializer = TicketSerializer(data=value)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(["GET"])
def getTicket(request):
    ticket_no = request.query_params.get('ticket_no')
    ticket = Ticket.objects.all()
    if ticket_no is not None:
        ticket=ticket.filter(ticket_no=ticket_no)
        serializer = TicketSerializer(ticket, many=True)
        total_department=len(serializer.data[0]["department"])
        total_assign=len(serializer.data[0]["agents_assigned"])
        for t in range(total_department):
            department=Department.objects.all().filter(id=serializer.data[0]["department"][t])
            serialiser=DepartmentSerializer(department,many=True)
            serializer.data[0]["department"].append(serialiser.data[0]["name"])
        for i in range(len(serializer.data[0]["agents_assigned"])): 
            assignee=Assignee.objects.all().filter(id=serializer.data[0]["agents_assigned"][i])
            serialiser=AssigneeSerializer(assignee,many=True)
            if(serialiser.data[0]["status"]=="Completed"):
                activity=Activity.objects.values().filter(ticket_id=serializer.data[0]["id"])
                serialiser.data[0]["remark"]=activity[0]["comments"]
                serialiser.data[0]["completed_at"]=activity[0]["closed_at"]
            member=Members.objects.values().filter(id=serialiser.data[0]["agent"])
            serialiser.data[0]["agent"]=member[0]["first_name"]+" "+member[0]["last_name"]
            serializer.data[0]["agents_assigned"].append(serialiser.data[0])
        for j in range(total_assign):
            serializer.data[0]["agents_assigned"].pop(0)
        for k in range(total_department):
            serializer.data[0]["department"].pop(0)
    return Response(serializer.data)
    
@api_view(['GET'])
def getDepartment(request):
    department = Department.objects.all()
    serializer = DepartmentSerializer(department, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request):
    room = Room.objects.all()
    serializer = RoomSerializer(room, many=True)
    return Response(serializer.data)

class EventAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
            "Buildings": 1,
            "Blocks": 2,
            "Floors": 3,
            "Rooms": 4,
            "Items": 5,
        }
        app_dict = self._build_app_dict(request)

        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        for app in app_list:
            app["models"].sort(key=lambda x: ordering[x["name"]])

        return app_list
