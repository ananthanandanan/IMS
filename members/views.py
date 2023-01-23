from django.shortcuts import render, redirect
from buildings.models import Ticket, Activity, ItemSwap
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from members.models import Members


from .forms import (
    ActivityForm,
    TicketFilter,
    TicketForm,
    ChangePasswordForm,
    RegisterForm,
    ActivityFilter,
    EditProfile,
)
from .utils import get_ip_address, ticketData, tableData, buildingWiseData, departmentPrice, itemWisedata
from userlog.models import UserLog
from buildings.models import Assignee

# importing HttpResponse
from django.shortcuts import render
from django.middleware import csrf
from django.forms.models import (
    inlineformset_factory,
)
from rest_framework.views import APIView
from rest_framework.response import Response


def register_member(request):
    """Register a new user

    Args:
        request (HttpRequest): The request object

    Returns:
        render: The register page
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            messages.success(request, "Account was created for " + email)
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "members/authenticate/register.html", {"form": form})


def login_member(request):
    """Login a user

    Args:
        request (HttpRequest): The request object

    Returns:
        render: The login page
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        ## If user exists, login and redirect to agent page or customer page
        if user is not None:
            ipAddress = get_ip_address(request)
            token = csrf.get_token(request)
            UserLog.objects.create(
                user=user, ipAddress=ipAddress, token=token, log_type="login"
            )
            login(request, user)
            if user.is_agent:
                return redirect("agent")
            else:
                return redirect("customer")
        ## If user does not exist, redirect to login page
        else:
            messages.info(request, "Username OR password is incorrect")
            return redirect("login")
    else:
        return render(request, "members/authenticate/login.html", {})


def change_password(request):
    """Change a user's password

    Args:
        request (HttpRequest): The request object

    Returns:
        render: The change password page
    """
    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password Changed Successfully")
            return redirect("login")
        else:
            messages.error(request, "Password Change Failed")
    else:
        form = ChangePasswordForm(user=request.user)
        args = {"form": form}
        return render(request, "members/authenticate/change_password.html", args)


def logout_member(request):
    """Logout a user

    Args:
        request (HttpRequest): The request object

    Returns:
        redirect: The login page
    """
    ipAddress = get_ip_address(request)
    token = csrf.get_token(request)
    UserLog.objects.create(
        user=request.user, ipAddress=ipAddress, token=token, log_type="logout"
    )
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def detail_ticket(request, ticket_id):
    """View details of a ticket and assign an agent to a ticket or remove an agent from a ticket

    Args:
        request (HttpRequest): The request object
        ticket_id (int): The id of the ticket

    Returns:
        render: The ticket details page
    """
    ticket = Ticket.objects.get(id=ticket_id)
    assigned_agent_data = []
    ## If ticket has an agent assigned, get the agent's email and department
    if ticket.agents_assigned.all().exists():
        ## Loop through the ticket's departments
        for department in ticket.department.all():
            ## If the ticket has an agent assigned to the department, get the agent's email and department
            if ticket.agents_assigned.filter(department=department).exists():
                assigned_agent = ticket.agents_assigned.filter(
                    department=department
                ).values("agent__email", "is_assigned", "status")
                assigned_agent_data.append(
                    {
                        "agent_email": assigned_agent[0]["agent__email"],
                        "is_assigned": assigned_agent[0]["is_assigned"],
                        "department": department.name,
                        "status": assigned_agent[0]["status"],
                    }
                )
            ## If the ticket does not have an agent assigned to the department, get the department and set is_assigned to False
            else:
                assigned_agent_data.append(
                    {
                        "agent_email": None,
                        "is_assigned": False,
                        "department": department.name,
                        "status": "Pending",
                    }
                )
    else:
        ## If ticket does not have an agent assigned, get the ticket's departments and set is_assigned to False
        for department in ticket.department.all():
            assigned_agent_data.append(
                {
                    "agent_email": None,
                    "is_assigned": False,
                    "department": department.name,
                    "status": "Pending",
                }
            )

    return render(
        request,
        "members/tickets/details.html",
        {"ticket_data": ticket, "assigned_agent_data": assigned_agent_data},
    )


@login_required(login_url="login")
def assign_agent(request, ticket_id, department: str):
    """Assign an agent to a ticket
    or remove an agent from a ticket.

    Args:
        request (HttpRequest): The request object
        ticket_id (int): The id of the ticket
        department (str): The name of the department

    Returns:
        redirect: The ticket details page
    """
    ticket = Ticket.objects.get(id=ticket_id)
    agent = Members.objects.get(email=request.user.email)

    ## If no agents are assigned to the ticket, assign the agent to the ticket
    if ticket.agents_assigned.all().exists() is False:
        if department in agent.department.all().values_list("name", flat=True):
            department = agent.department.get(name=department)
            assigned_agent = Assignee.objects.create(
                agent=agent, is_assigned=True, department=department
            )
            ticket.agents_assigned.add(assigned_agent)
            ticket.save()
            messages.success(request, "Agent assigned to ticket")
            return redirect("detail_ticket", ticket_id=ticket_id)
        else:
            messages.error(request, "You are not assigned to this department")
            return redirect("detail_ticket", ticket_id=ticket_id)
    ## If agent is already assigned to the ticket, remove the agent from the ticket,
    ## only if the agent is assigned to the department clicked on.
    ## Also, if agent is part of more than one department, assign the agent to the ticket, only if the agent is assigned to the department clicked on.
    elif (
        department in agent.department.all().values_list("name", flat=True)
        and ticket.agents_assigned.filter(
            agent=agent, department__name=department
        ).exists()
    ):
        assigned_agent = Assignee.objects.get(
            agent=agent,
            is_assigned=True,
            agents_assigned=ticket.id,
            department__name=department,
        )
        ticket.agents_assigned.remove(assigned_agent.id)
        Assignee.objects.filter(id=assigned_agent.id).delete()
        ticket.save()
        messages.success(request, "Agent removed from ticket")
        return redirect("detail_ticket", ticket_id=ticket_id)
    ## If agent is not assigned to the ticket, assign the agent to the ticket
    ## only if agent department is the same as the department clicked on.
    ## Also, check if the ticket has already been assigned to the maximum number of agents
    ## (the number of agents assigned to the ticket should be equal to the number of departments the ticket is assigned to)
    ## Agent already assigned ticket of a department, but current click is for a different department, so assign agent to ticket
    elif (
        department in agent.department.all().values_list("name", flat=True)
        and not ticket.agents_assigned.filter(
            agent=agent, department__name=department
        ).exists()
        and ticket.agents_assigned.all().count() < ticket.department.all().count()
    ):
        department = agent.department.get(name=department)
        assigned_agent = Assignee.objects.create(
            agent=agent, is_assigned=True, department=department
        )
        ticket.agents_assigned.add(assigned_agent)
        ticket.save()
        messages.success(request, "Agent assigned to ticket")
        return redirect("detail_ticket", ticket_id=ticket_id)
    else:
        messages.error(
            request,
            "You are not assigned to this department/ticket already assigned to maximum agents",
        )
        return redirect("detail_ticket", ticket_id=ticket_id)


@login_required(login_url="login")
def agent(request):
    """View all tickets for an agent

    Args:
        request (HttpRequest): The request object

    Returns:
        render: The agent dashboard page
    """
    dept = request.user.department.all().values_list("name", flat=True)
    tickets = (
        Ticket.objects.all()
        .filter(status="Pending", department__name__in=dept)
        .distinct()
        .order_by("created_at")
        .reverse()
    )
    ticketFilter = TicketFilter(request.GET, queryset=tickets)
    tickets = ticketFilter.qs
    p = Paginator(tickets, 10)
    page = request.GET.get("page")
    tickets_p = p.get_page(page)
    return render(
        request,
        "members/agent/index.html",
        {"agent_data": tickets, "ticketFilter": ticketFilter, "tickets_p": tickets_p},
    )


@login_required(login_url="login")
def customer(request):
    """View all tickets for a customer

    Args:
        request (HttpRequest): The request object

    Returns:
        render: The customer dashboard page
    """
    customer_name = request.user
    tickets = (
        Ticket.objects.all()
        .filter(status="Pending", created_by=customer_name)
        .order_by("created_at")
        .reverse()
    )
    ticketFilter = TicketFilter(request.GET, queryset=tickets)
    tickets = ticketFilter.qs

    p = Paginator(tickets, 10)
    page = request.GET.get("page")
    tickets_p = p.get_page(page)
    return render(
        request,
        "members/customer/index.html",
        {
            "customer_data": tickets,
            "ticketFilter": ticketFilter,
            "tickets_p": tickets_p,
        },
    )


@login_required(login_url="login")
def activity(request):
    """View all activities

    Args:
        request (HttpRequest): The request object

    Returns:
        render: The activity dashboard page
    """
    activity = Activity.objects.all().order_by("closed_at").reverse()
    activityFilter = ActivityFilter(request.GET, queryset=activity)
    activity = activityFilter.qs

    p = Paginator(activity, 10)
    page = request.GET.get("page")
    activities = p.get_page(page)

    return render(
        request,
        "members/activity/index.html",
        {
            "activity_data": activity,
            "activityFilter": activityFilter,
            "activities": activities,
        },
    )


@login_required(login_url="login")
def detail_activity(request, activity_id):
    """View details of an activity

    Args:
        request (HttpRequest): The request object

    Returns:
        render: The activity details page

    """
    activity = Activity.objects.get(id=activity_id)
    swap_items = ItemSwap.objects.all().filter(activity=activity_id)
    return render(
        request,
        "members/activity/details.html",
        {"activity_data": activity, "item_data": swap_items},
    )


@login_required(login_url="login")
def create_ticket(request):
    """Create a new ticket

    Args:
        request (HttpRequest): The request object

    Returns:
        render: The create ticket page

    """
    if request.method == "POST":

        form = TicketForm(
            request.POST,
            initial={"created_by": request.user.pk, "room": request.user.room_no.pk},
        )
        if form.is_valid():
            form.save()
            message = form.cleaned_data.get("maintenance")
            room = form.cleaned_data.get("room")
            department = form.cleaned_data.get("department")
            created_by = form.cleaned_data.get("created_by")
            comment = form.cleaned_data.get("message")
            messages.success(request, "Ticket Created Successfully")

            return redirect("customer")

    else:
        form = TicketForm(
            initial={"created_by": request.user, "room": request.user.room_no}
        )
    return render(request, "members/customer/ticket.html", {"form": form})


@login_required(login_url="login")
def activityCreation(request,ticket_no):
    """Activity Creation Form

    Args:
        request (HttpRequest): The request object

    Returns:
        render: The activity creation page

    """
    ActivityFormSet = inlineformset_factory(
        Activity, ItemSwap, fields="__all__", extra=0, can_delete=False
    )
    agent = Members.objects.get(email=request.user.email)
    ticket= Ticket.objects.get(ticket_no=ticket_no)
    if request.method == "POST":
        form = ActivityForm(request.POST or None, agent=agent, initial={'ticket':ticket})
        formset = ActivityFormSet(request.POST or None)
        if form.is_valid() and formset.is_valid():
            activity = form.save()
            ## Check if all the departments have completed the activity
            ## If yes, change the status of the ticket to completed
            ticket = Ticket.objects.get(activity=activity)
            assigned_agent = Assignee.objects.get(
                agent=agent, is_assigned=True, agents_assigned=ticket.id
            )
            assigned_agent.status = "Completed"
            assigned_agent.save()
            if ticket.activity_set.all().count() == ticket.department.all().count():
                ticket.status = "Completed"

                ticket.save()
            for form in formset.forms:
                item = form.save(commit=False)
                item.activity = activity
                item.save()
            messages.success(request, "Activity Created Successfully")
            return redirect("activity")

        else:
            messages.error(request, "Activity Creation Failed")
            return redirect("activity")
    else:
        form = ActivityForm(request.POST or None, agent=agent)
        formset = ActivityFormSet()

        return render(
            request,
            "members/agent/activityform.html",
            {"form": form, "formset": formset},
        )


class reportAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data = ticketData()
        return Response(data)


class tableAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data = tableData()

        return Response(data)


class buildingAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data = buildingWiseData()

        return Response(data)

class departmentPriceAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data = departmentPrice()

        return Response(data)
class itemPriceAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data = itemWisedata()

        return Response(data)

class departmentPriceAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data = departmentPrice()

        return Response(data)
class itemPriceAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data = itemWisedata()

        return Response(data)
def report(request):
    """report page

    Args:
        request (HttpRequest): The request object

    Returns:
        render: The report page
    """
    report_data = list(ticketData())
    # report_data = dumps(report_data)
    return render(request, "members/report/index.html")


@login_required(login_url="login")
def profile(request):
    """Profile page

    Args:

        request (HttpRequest): The request object

    Returns:
        render: The profile page

    """
    form = EditProfile(request.POST or None, instance=request.user)
    userTickets = Ticket.objects.filter(created_by=request.user)
    if form.is_valid():
        form.save()
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        email = form.cleaned_data.get("email")
        room_no = form.cleaned_data.get("room_no")

        # update tickets created by the user
        userTickets.update(room=room_no)
        userTickets.update(created_by=request.user)
        messages.success(request, "Profile Updated Successfully")

        return redirect("customer")
    return render(request, "members/customer/profile.html", {"form": form})
