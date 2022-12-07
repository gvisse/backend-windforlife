from .models import Anemometer
from .serializers import AnemometerSerializer

from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q, Avg

from rest_framework import viewsets, permissions

class AnemometerViewSet(viewsets.ModelViewSet):

    serializer_class = AnemometerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # initialization of variables for time range
        today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
        today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
        week_min = datetime.combine(timezone.now().date() - timedelta(weeks=1), (datetime.today()-timedelta(weeks=1)).time().min)

        queryset = Anemometer.objects.all().prefetch_related('tags')
        mean_speed_today = Avg('winds__speed', filter=Q(winds__time__range=(today_min, today_max)))
        mean_speed_week = Avg('winds__speed', filter=Q(winds__time__range=(week_min, today_max)))
        queryset = queryset.annotate(mean_speed_today=mean_speed_today, mean_speed_week=mean_speed_week)

        tags = self.request.GET.get('tags')
        if tags:
            tags = tags.split(',')
            queryset = queryset.filter(tags__name__in=tags)

        return queryset
