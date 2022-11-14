from rest_framework import serializers

from tag.models import Tag
from tag.serializers import TagSerializer
from .models import Anemometer

class AnemometerSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)

    class Meta:
        model = Anemometer
        fields = [
            'id', 'name', 'latitude', 'longitude',
            'altitude', 'tags']