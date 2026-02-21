from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from events.models import Event, TicketLead


@login_required
def dashboard_view(request):
    # SUMMARY COUNTS
    total_events = Event.objects.count()
    active_events = Event.objects.filter(status__in=["new", "updated"]).count()
    inactive_events = Event.objects.filter(status="inactive").count()
    imported_events = Event.objects.filter(status="imported").count()
    total_leads = TicketLead.objects.count()

    # FILTERS
    status_filter = request.GET.get("status")
    city_filter = request.GET.get("city")

    events = Event.objects.all().order_by("-last_scraped_at")

    if status_filter:
        events = events.filter(status=status_filter)

    if city_filter:
        events = events.filter(city__icontains=city_filter)

    leads = TicketLead.objects.select_related("event").order_by("-created_at")

    # ✅ ADD THIS (IMPORTANT)
    status_chart = {
        "new": Event.objects.filter(status="new").count(),
        "updated": Event.objects.filter(status="updated").count(),
        "inactive": Event.objects.filter(status="inactive").count(),
        "imported": Event.objects.filter(status="imported").count(),
    }

    context = {
        "total_events": total_events,
        "active_events": active_events,
        "inactive_events": inactive_events,
        "imported_events": imported_events,
        "total_leads": total_leads,
        "events": events[:20],
        "leads": leads[:20],
        "status_chart": status_chart,
    }

    return render(request, "dashboard/dashboard.html", context)


@login_required
def import_event(request, event_id):
    """
    Mark event as imported (assignment requirement)
    """
    event = get_object_or_404(Event, id=event_id)
    event.status = "imported"
    event.save()

    return redirect("dashboard")