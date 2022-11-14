from .views import WindViewSet

from django.urls import path, include

from rest_framework import routers

router = routers.SimpleRouter()
router.register('wind', WindViewSet, basename='wind')

urlpatterns = [
    path('', include(router.urls)),
]