from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("buildings/", views.index, name="index"),
    path("tickets_get/", views.getTicket, name="getTicket"),
    path("tickets_post/", views.postTicket, name="postTicket"),
    path("get_department/", views.getDepartment, name="department"),
    path("get_room/", views.getRoom, name="room"),
]
