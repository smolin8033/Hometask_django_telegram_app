from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from config.loggers import logger
from groups.user_groups import students_group, teachers_group
from users.models import TelegramUser
from users.serializers import TelegramUserSerializer


@extend_schema(tags=["Пользователи телеграма"])
class TelegramUserViewSet(ModelViewSet):
    serializer_class = TelegramUserSerializer

    def get_queryset(self):
        logger.info(f"в кверисете {self.request.user}")
        # queryset = TelegramUser.objects.prefetch_related("telegram_users").all()
        queryset = TelegramUser.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        headers["Role"] = request.headers["Role"]

        self.add_to_group(headers, instance)
        self.make_active(instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance: TelegramUser = serializer.save()
        return instance

    @staticmethod
    def add_to_group(headers, instance: TelegramUser):
        if headers["Role"] == "teacher":
            instance.groups.add(teachers_group)
        elif headers["Role"] == "student":
            instance.groups.add(students_group)
        instance.save()
        return instance

    @staticmethod
    def make_active(instance: TelegramUser):
        instance.is_active = True
        instance.save()
        return instance
