from rest_framework.routers import DefaultRouter

from .viewsets import TelegramUserViewSet

router = DefaultRouter()
router.register("telegram_users", TelegramUserViewSet, basename="telegram_users")
