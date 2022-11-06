from rest_framework.routers import DefaultRouter

from .viewsets import HometaskFileViewSet, HometaskImageViewSet, HometaskViewSet

router = DefaultRouter()
router.register("hometasks", HometaskViewSet, basename="hometasks")
router.register("images", HometaskImageViewSet, basename="images")
router.register("files", HometaskFileViewSet, basename="files")
