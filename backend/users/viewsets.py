from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from config.loggers import logger
from users.models import TelegramUser
from users.serializers import TelegramUserSerializer


@extend_schema(tags=["Пользователи телеграма"])
class TelegramUserViewSet(ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer

    def create(self, request, *args, **kwargs):
        logger.info(request.data)
        serializer = self.get_serializer(data=request.data)
        logger.info(serializer.initial_data)
        serializer.is_valid(raise_exception=True)
        logger.info(serializer.validated_data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
