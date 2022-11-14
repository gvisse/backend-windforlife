from rest_framework import serializers

from tag.models import Tag
from tag.serializers import TagSerializer
from .models import Anemometer

class AnemometerSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)
    mean_speed_today = serializers.FloatField(read_only=True)
    mean_speed_week = serializers.FloatField(read_only=True)

    class Meta:
        model = Anemometer
        fields = [
            'id', 'name', 'latitude', 'longitude',
            'altitude', 'tags', 'mean_speed_today', 'mean_speed_week']

    def validate_tags(self, data):
        return data 

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        anemometer = Anemometer.objects.create(**validated_data)
        if tags:
            names = [tag['name'] for tag in tags]
            for name in names:
                if not Tag.objects.filter(name=name).exists():
                    Tag.objects.create(name=name)
            tags = Tag.objects.filter(name__in=names)
            anemometer.tags.set(tags)
        return anemometer

    def update(self, instance, validated_data):
        if 'tags' in validated_data.keys():
            # replacement of tags if the key is in posted data
            tags = validated_data.pop('tags')
            for tag in tags:
                object_tag, created = Tag.objects.get_or_create(name=tag['name'])
            tags_objects = Tag.objects.filter(name__in=[tag['name'] for tag in tags])
            instance.tags.set(tags_objects)
        instance = super(AnemometerSerializer, self).update(instance, validated_data)
        return instance