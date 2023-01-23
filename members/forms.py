from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.forms import ModelForm
from .models import Members
from buildings.models import *
import django_filters


class RegisterForm(UserCreationForm):
    class Meta:
        model = Members
        fields = ["email", "password1", "password2", "first_name", "last_name"]

    email = forms.EmailField(
        label="Email",
        max_length=100,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    password1 = forms.CharField(
        label="Password",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = Members
        fields = ["old_password", "new_password1", "new_password2"]

    old_password = forms.CharField(
        label="Old Password",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Old Password"}
        ),
    )
    new_password1 = forms.CharField(
        label="New Password",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New Password"}
        ),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm New Password"}
        ),
    )


## Ticket Filter Form


class TicketFilter(django_filters.FilterSet):
    maintenance = django_filters.ModelChoiceFilter(
        queryset=Maintenance.objects.all(),
        widget=forms.Select(attrs={"class": "form-control-sm mx-2"}),
        label="Maintenance",
    )
    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={"class": "form-control-sm mx-2"}),
        label="Department",
    )
    room = django_filters.ModelChoiceFilter(
        queryset=Room.objects.all(),
        widget=forms.Select(attrs={"class": "form-control-sm mx-2"}),
        label="Room",
    )
    status = django_filters.ChoiceFilter(
        choices=Ticket.STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-control-sm mx-2"}),
        label="Status",
    )

    class Meta:
        model = Ticket
        fields = ["maintenance", "department", "room", "status"]


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["maintenance", "room", "department", "created_by", "message"]

    created_by = forms.ModelChoiceField(
        queryset=Members.objects.filter(),
        widget=forms.HiddenInput(),
        disabled=True,
    )
    maintenance = forms.ModelChoiceField(
        queryset=Maintenance.objects.all(),
        widget=forms.HiddenInput(),
        initial="",
        required=False,
    )
    department = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control w-25 scrollable h-25"}
        ),
        label="Department",
        required=True,
    )
    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        widget=forms.HiddenInput(),
        label="Room",
    )

    message = forms.CharField(
        label="Query",
        max_length=100,
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Enter your message here"}
        ),
    )


class ActivityForm(ModelForm):
    def __init__(self, *args, **kwargs):

        self.agent = kwargs.pop("agent")
        super().__init__(*args, **kwargs)

        self.fields["ticket"].queryset = Ticket.objects.all().filter(
            status="Pending", agents_assigned__agent=self.agent
        )

    class Meta:
        model = Activity
        fields = ["ticket", "comments"]

    ticket = forms.ModelChoiceField(
        queryset=Ticket.objects.all(),
        widget=forms.HiddenInput(),
        disabled=True,
    )


class ActivityFilter(django_filters.FilterSet):
    ticket = django_filters.ModelChoiceFilter(
        queryset=Ticket.objects.all(),
        widget=forms.Select(attrs={"class": "form-control-sm mx-2"}),
        label="Ticket",
    )


class EditProfile(forms.ModelForm):
    class Meta:
        model = Members
        fields = ["first_name", "last_name", "email", "room_no"]

    first_name = forms.CharField(
        label="First Name",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        max_length=100,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    room_no = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Room",
            }
        ),
        label="Room",
    )
