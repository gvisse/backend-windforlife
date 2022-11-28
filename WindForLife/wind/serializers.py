from .models import Wind
from anemometer.models import Anemometer

from rest_framework import serializers


class WindSerializer(serializers.ModelSerializer):

    anemometer_id = serializers.PrimaryKeyRelatedField(queryset=Anemometer.objects.all())

    class Meta:
        model = Wind
        fields = ['id', 'speed', 'time', 'direction', 'cardinal', 'anemometer_id']

    def validate_anemometer_id(self, data):
        return data.id

class WindStatsSerializer(serializers.ModelSerializer):

    min = serializers.FloatField(read_only=True)
    max = serializers.FloatField(read_only=True)
    mean = serializers.FloatField(read_only=True)

    class Meta:
        model = Wind
        fields= ['min', 'max', 'mean']