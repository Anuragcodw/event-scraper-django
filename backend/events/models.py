from django.db import models


class Event(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('updated', 'Updated'),
        ('inactive', 'Inactive'),
        ('imported', 'Imported'),
    ]

    title = models.CharField(max_length=255)
    date_time = models.DateTimeField()

    venue_name = models.CharField(max_length=255, blank=True)
    venue_address = models.TextField(blank=True)
    city = models.CharField(max_length=100, default="Sydney")

    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)

    image_url = models.URLField(blank=True)
    source_website = models.CharField(max_length=100)
    original_event_url = models.URLField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    last_scraped_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TicketLead(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    email = models.EmailField()
    consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.event.title}"