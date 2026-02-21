from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("dashboard/import/<int:event_id>/", views.import_event, name="import_event"),
]