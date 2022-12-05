from .models import Wind
from .serializers import WindSerializer, WindStatsSerializer

import geopy

from django.db.models import Avg, Min, Max, FloatField

from rest_framework import views, viewsets, permissions
from rest_framework.response import Response


class WindViewSet(viewsets.ModelViewSet):

    serializer_class = WindSerializer
    permission_classes = []
    
    def get_queryset(self):
        queryset = Wind.objects.all()
        anemometer_id = self.request.GET.get('anemometer_id')
        if anemometer_id is not None:
            queryset = queryset.filter(anemometer__id=anemometer_id)
        return queryset


class WindStatsView(views.APIView):

    permission_classes = []

    def get(self, *args, **kwargs):
        queryset = Wind.objects.all()
        central_point = self.request.GET.get('central_point')
        radius = self.request.GET.get('radius')
        if central_point is not None and radius is not None:
            central_point = tuple(central_point.split(','))
            rough_distance = geopy.units.degrees(arcminutes=geopy.units.nautical(miles=float(radius)))
            # filter latitude range and longitude range between central_point and a conversion of radius in decimal degrees
            queryset = queryset.filter(
                    anemometer__latitude__range=(float(central_point[0]) - rough_distance, float(central_point[0]) + rough_distance),
                    anemometer__longitude__range=(float(central_point[1]) - rough_distance, float(central_point[1]) + rough_distance)
                )
        serializer = WindStatsSerializer(queryset.aggregate(
                    min=Min('speed', output_field=FloatField()),
                    max=Max('speed', output_field=FloatField()),
                    mean=Avg('speed', output_field=FloatField())
                ), many=False)
        return Response(serializer.data)