from django.urls import path
from . import views

urlpatterns = [
    path("events/", views.browse_events, name="browse_events"),
    path("api/events/", views.event_list),
    path("api/get-tickets/", views.get_tickets),
]