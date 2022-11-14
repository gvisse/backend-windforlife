from .views import WindViewSet, WindStatsView

from django.urls import path, include

from rest_framework import routers

router = routers.SimpleRouter()
router.register('wind', WindViewSet, basename='wind')

urlpatterns = [
    path('', include(router.urls)),
    path('wind-stats/', WindStatsView.as_view()),
]