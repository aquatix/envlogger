from django.core.management.base import BaseCommand
from weather.actions import update_everything

class Command(BaseCommand):
    help = 'Update all enabled weather providers, creating new Observations'

    def handle(self, *args, **options):
        update_everything()

        # TODO: log
        #self.stdout.write(self.style.SUCCESS('Successfully updated everything'))

