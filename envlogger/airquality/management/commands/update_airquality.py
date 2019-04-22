from django.core.management.base import BaseCommand
from airquality.actions import update_airquality

class Command(BaseCommand):
    help = 'Update all enabled air quality locations, creating new AQIObservations'

    def handle(self, *args, **options):
        update_airquality()
