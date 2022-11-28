from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from anemometer.models import Anemometer

class Wind(models.Model):

    class Meta:
        db_table = 'api_wind'
        verbose_name = 'Mesure de vitesse du vent'
        unique_together = ['speed', 'time', 'anemometer']

    speed = models.FloatField(verbose_name='vitesse (en nœuds)')
    time = models.DateTimeField(verbose_name='date de la mesure')
    direction = models.FloatField(verbose_name='direction en degré', validators=[MinValueValidator(0.0), MaxValueValidator(360)],)
    # if an anemometer is deleted, all associated wind measurements are deleted
    anemometer = models.ForeignKey(Anemometer, on_delete=models.CASCADE, related_name='winds')

    def __str__(self):
        return f'{self.anemometer.name} : {self.speed} ({self.__get_direction__}) à {self.time}'

    @property
    def cardinal(self):
        cardinals = {
            0 : 'N',  11.25: 'NbE', 22.5: 'NNE', 33.75: 'NEbN',
            45: 'NE', 56.25: 'NEbE', 67.5: 'ENE', 78.75: 'EbN',
            90: 'E', 101.25: 'EbS', 112.5: 'ESE', 123.75: 'SEbE',
            135: 'SE', 146.25: 'SEbS', 157.5: 'SSE', 168.75: 'SbE',
            180: 'S', 191.25: 'SbW', 202.5: 'SSW', 213.75: 'SWbS',
            225: 'SW', 236.25: 'SWbW', 247.5: 'WSW', 258.75: 'WbS',
            270: 'W', 281.25: 'WbN', 292.5: 'WNW', 303.75: 'NWbW',
            315: 'NW', 326.25: 'NWbN', 337.5: 'NNW', 348.75: 'NbW',
            360: 'N'
        }
        key, val = min(cardinals.items(), key=lambda x: abs(self.direction - x[0]))
        return val
