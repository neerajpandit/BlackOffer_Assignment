# import_energy_data.py
import json
from django.core.management.base import BaseCommand
from main.models import EnergyInsight
from datetime import datetime
import pytz
class Command(BaseCommand):
    help = 'Import energy data into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            with open(file_path, 'r', encoding='utf-8') as file:  # Specify the encoding here
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON file format'))
            return

        for item in data:
            intensity_str = item.get('intensity', '')
            likelihood_str = item.get('likelihood', '')
            relevance_str = item.get('relevance', '')
            try:
                # Attempt to convert to integer
                relevance = int(relevance_str) if relevance_str else None
                item['relevance'] = relevance
                likelihood = int(likelihood_str) if likelihood_str else None
                item['likelihood'] = likelihood
                intensity = int(intensity_str) if intensity_str else None
                item['intensity'] = intensity
            except ValueError:
                # Handle the case where intensity is not a valid integer
                self.stdout.write(self.style.ERROR(f'Invalid intensity value: {intensity_str}'))
                continue
            # Convert string to datetime using the specified format
            # Check if datetime strings are not empty before conversion
            added_str = item.get('added', '')
            published_str = item.get('published', '')

            if added_str:
                added = datetime.strptime(added_str, '%B, %d %Y %H:%M:%S')
                added = added.replace(tzinfo=pytz.UTC)
                item['added'] = added
            else:
                item['added'] = None

            if published_str:
                published = datetime.strptime(published_str, '%B, %d %Y %H:%M:%S')
                published = published.replace(tzinfo=pytz.UTC)
                item['published'] = published
            else:
                item['published'] = None
            EnergyInsight.objects.create(**item)

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
