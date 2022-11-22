from django.db import models
from tag.models import Tag
class Anemometer(models.Model):

    class Meta:
        db_table = 'api_anemometer'
        verbose_name = 'Anemomètre'
        unique_together = ['latitude', 'longitude', 'altitude']

    name = models.CharField(verbose_name='nom', max_length=255)
    latitude = models.DecimalField(verbose_name='latitude', max_digits=9, decimal_places=7, null=False)
    longitude = models.DecimalField(verbose_name='longitude', max_digits=10, decimal_places=7, null=False)
    altitude = models.IntegerField(verbose_name='altitude(en m)', null=False)
    tags = models.ManyToManyField(Tag, related_name='tags')

    def __str__(self):
        tags = ','.join([tag.name for tag in self.tags.all()])
        return f'{self.name} ({tags}) : lat={self.latitude}, long={self.longitude}, alt={self.altitude}'