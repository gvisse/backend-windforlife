from django.db import models

class Tag(models.Model):

    class Meta:
        verbose_name = 'Tag'

    name = models.CharField(verbose_name='nom', max_length=255, unique=True)

    def __str__(self):
        return self.name