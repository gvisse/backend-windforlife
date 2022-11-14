from .models import Anemometer
from .serializers import AnemometerSerializer

from rest_framework import viewsets, permissions

class AnemometerViewSet(viewsets.ModelViewSet):

    serializer_class = AnemometerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Anemometer.objects.all().prefetch_related('tags')
        return queryset
