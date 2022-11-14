from .models import Wind
from .serializers import WindSerializer

from rest_framework import viewsets, permissions


class WindViewSet(viewsets.ModelViewSet):

    serializer_class = WindSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Wind.objects.all()
        anemometer_id = self.request.GET.get('anemometer_id')
        if anemometer_id is not None:
            queryset = queryset.filter(anemometer__id=anemometer_id)
        return queryset
