from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Event, TicketLead
import json


# ----------------------------
# HOME PAGE
# ----------------------------
def home(request):
    """
    Landing page
    """
    return render(request, "home.html")


# ----------------------------
# EVENTS LIST API (BACKEND)
# ----------------------------
def event_list(request):
    """
    Returns list of active events (API)
    Public API – login NOT required
    """
    events = Event.objects.filter(
        status__in=["new", "updated"]
    ).order_by("-date_time")

    data = []
    for e in events:
        data.append({
            "id": e.id,
            "title": e.title,
            "date_time": e.date_time.strftime("%Y-%m-%d %H:%M"),
            "venue": e.venue_name,
            "city": e.city,
            "description": e.description,
            "source": e.source_website,
            "original_url": e.original_event_url,
        })

    return JsonResponse({"events": data})


# ----------------------------
# EVENTS PAGE (LOGIN REQUIRED)
# ----------------------------
@login_required(login_url="/accounts/google/login/")
def browse_events(request):
    """
    User-facing events page
    Login required → redirects to Google OAuth
    """
    events = Event.objects.filter(
        status__in=["new", "updated"]
    ).order_by("-date_time")

    return render(request, "events.html", {
        "events": events
    })


# ----------------------------
# GET TICKETS API
# ----------------------------
@csrf_exempt
def get_tickets(request):
    """
    Save email + consent, then redirect
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    body = json.loads(request.body)
    email = body.get("email")
    consent = body.get("consent")
    event_id = body.get("event_id")

    if not email or not consent:
        return JsonResponse(
            {"error": "Email & consent required"},
            status=400
        )

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse(
            {"error": "Event not found"},
            status=404
        )

    # ✅ SAVE LEAD
    TicketLead.objects.create(
        event=event,
        email=email,
        consent=consent
    )

    return JsonResponse({
        "redirect_url": event.original_event_url
    })