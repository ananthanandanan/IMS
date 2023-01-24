"""ims URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from members import views

# from buildings.views import ArticleView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("building/", include("buildings.urls")),
    path(
        "members/", include("django.contrib.auth.urls")
    ),  ## login/logout functionality from django
    path("members/", include("members.urls")),
    path("graph_api", views.reportAPI.as_view()),
    path("table_api", views.tableAPI.as_view()),
    path("buildingWise_api", views.buildingAPI.as_view()),
    path("itemWise_api", views.departmentPriceAPI.as_view()),
    path("itemPrice_api", views.itemPriceAPI.as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
