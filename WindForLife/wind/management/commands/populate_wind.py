from django.core.management.base import BaseCommand, CommandError
from anemometer.models import Anemometer
from wind.models import Wind

import requests
import datetime


class Command(BaseCommand):

    help = 'Populate winds for every anemometers'

    def handle(self, *args, **options):
        anemometers = Anemometer.objects.all()
        for anemo in anemometers:
            created = 0
            url_request = f'https://api.open-meteo.com/v1/forecast?latitude={anemo.latitude}&longitude={anemo.longitude}&hourly=windspeed_10m,winddirection_10m&windspeed_unit=kn&timezone=auto'
            response = requests.get(url_request)
            if response.status_code not in (200, 201):
                self.stdout.write(self.style.ERROR(f'Today\'s winds for {anemo} was unreachable'))
                continue
            else:
                data = response.json()
                for i in range(len(data['hourly']['time'])):
                    if datetime.datetime.fromisoformat(data['hourly']['time'][i]) <= datetime.datetime.now():
                        wind = Wind.objects.create(
                            speed=data['hourly']['windspeed_10m'][i],
                            time=data['hourly']['time'][i],
                            direction=data['hourly']['winddirection_10m'][i],
                            anemometer=anemo
                            )
                        created += 1
            self.stdout.write(self.style.SUCCESS(f'{created} winds created on {anemo}'))
        
                    