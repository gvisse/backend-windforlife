from .models import Tag
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):

    anemos__count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'anemos__count']
        extra_kwargs = {
            'name': {'validators': []},
        }