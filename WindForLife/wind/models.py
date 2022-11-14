from django.db import models

from anemometer.models import Anemometer

class Wind(models.Model):

    class Meta:
        verbose_name = 'Mesure de vitesse du vent'
        unique_together = ['speed', 'time', 'anemometer']

    speed = models.FloatField(verbose_name='vitesse (en nœuds)')
    time = models.DateTimeField(verbose_name='date de la mesure')
    # if an anemometer is deleted, all associated wind measurements are deleted
    anemometer = models.ForeignKey(Anemometer, on_delete=models.CASCADE, related_name='winds')

    def __str__(self):
        return f'{self.anemometer.name} : {self.speed} à {self.time}'
