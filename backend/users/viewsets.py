from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from users.models import TelegramUser
from users.serializers import TelegramUserSerializer


@extend_schema(tags=["Пользователи телеграма"])
class TelegramUserViewSet(ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer


class Some(ModelViewSet):
    pass
