from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from django.utils import timezone
from .models import Event
import time


SOURCE_URL = "https://www.eventbrite.com/d/australia--sydney/events/"
SOURCE_NAME = "Eventbrite"
CITY = "Sydney"


def scrape_events():
    print("Scraping started with Selenium...")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(SOURCE_URL)
        time.sleep(6)  # allow JS content to load

        # 1️⃣ Mark previously scraped events as inactive
        Event.objects.filter(
            city=CITY,
            source_website=SOURCE_NAME
        ).update(status="inactive")

        event_elements = driver.find_elements(By.TAG_NAME, "h3")
        saved_count = 0

        for event in event_elements[:5]:  # demo limit
            title = event.text.strip()
            if not title:
                continue

            obj, created = Event.objects.get_or_create(
                title=title,
                city=CITY,
                source_website=SOURCE_NAME,
                defaults={
                    "date_time": timezone.now(),
                    "venue_name": "",
                    "description": "",
                    "original_event_url": SOURCE_URL,
                    "status": "new"
                }
            )

            # 2️⃣ Status lifecycle
            obj.status = "new" if created else "updated"
            obj.last_scraped_at = timezone.now()
            obj.save()

            saved_count += 1

        print(f"Scraping completed. Events saved/updated: {saved_count}")

    finally:
        driver.quit()