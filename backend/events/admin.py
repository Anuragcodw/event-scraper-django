from django.contrib import admin
from .models import Event, TicketLead


# ----------------------------
# EVENT ADMIN (Already good, polished)
# ----------------------------
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'date_time',
        'city',
        'status',
        'source_website',
        'last_scraped_at'
    )

    list_filter = (
        'city',
        'status',
        'source_website'
    )

    search_fields = (
        'title',
        'venue_name',
        'description'
    )

    ordering = ('-last_scraped_at',)


# ----------------------------
# TICKET LEAD ADMIN (PART C ADDITION)
# ----------------------------
@admin.register(TicketLead)
class TicketLeadAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'event',
        'consent',
        'created_at'
    )

    list_filter = (
        'consent',
        'created_at'
    )

    search_fields = (
        'email',
        'event__title'
    )

    ordering = ('-created_at',)