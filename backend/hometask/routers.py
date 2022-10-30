from rest_framework.routers import DefaultRouter

from .viewsets import HometaskViewSet

router = DefaultRouter()
router.register("hometasks", HometaskViewSet, basename="hometasks")
