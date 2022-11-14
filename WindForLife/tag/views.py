from .models import Tag
from .serializers import TagSerializer

from rest_framework import viewsets, permissions

class TagViewSet(viewsets.ModelViewSet):

    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.all()