from .models import Wind
from anemometer.models import Anemometer

from rest_framework import serializers


class WindSerializer(serializers.ModelSerializer):

    anemometer = serializers.PrimaryKeyRelatedField(queryset=Anemometer.objects.all())

    class Meta:
        model = Wind
        fields = ['speed', 'time', 'anemometer']