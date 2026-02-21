from django.contrib import admin
from django.urls import path, include
from events import views as event_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),

    # ✅ HOME PAGE (ROOT)
    path("", event_views.home, name="home"),

    # EVENTS & API
    path("", include("events.urls")),

    # DASHBOARD
    path("dashboard/", include("dashboard.urls")),
]