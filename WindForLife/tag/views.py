from .models import Tag
from .serializers import TagSerializer

from rest_framework import viewsets, permissions
from django.db.models import Count

class TagViewSet(viewsets.ModelViewSet):

    serializer_class = TagSerializer
    permission_classes = []

    def get_queryset(self):
        return Tag.objects.all().annotate(anemos__count=Count('anemos')).order_by('name')