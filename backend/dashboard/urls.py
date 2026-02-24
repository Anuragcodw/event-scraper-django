from django.urls import path
from . import views

urlpatterns = [
   
    path("", views.dashboard_view, name="dashboard"),

    path("import/<int:event_id>/", views.import_event, name="import_event"),
]