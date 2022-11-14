from django.urls import path, include

from rest_framework import routers

router = routers.SimpleRouter()
router.register('anemometer', AnemometerViewSet, basename='anemometer')

urlpatterns = [
    path('', include(router.urls)),
]