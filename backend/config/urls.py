from django.contrib import admin
from django.urls import path, include
from events import views as event_views

urlpatterns = [
   
    path("admin/", admin.site.urls),

    path("accounts/", include("allauth.urls")),

    path("", event_views.home, name="home"),

    path("", include("events.urls")),

    path("dashboard/", include("dashboard.urls")),
]