from .views import *

from django.urls import path, include

from rest_framework import routers

router = routers.SimpleRouter()
router.register('tag', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
]