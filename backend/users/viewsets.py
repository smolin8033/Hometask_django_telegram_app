from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from groups.user_groups import students_group, teachers_group
from users.models import TelegramUser
from users.serializers import TelegramUserSerializer


@extend_schema(tags=["Пользователи телеграма"])
class TelegramUserViewSet(ModelViewSet):
    serializer_class = TelegramUserSerializer

    def get_queryset(self):
        user_group: str = self.request.user.groups.first().name

        mapper = {"Teachers": "Students", "Students": "Teachers"}

        group_name: str = mapper.get(user_group)

        queryset = (
            TelegramUser.objects.prefetch_related("telegram_users")
            .prefetch_related("groups")
            .prefetch_related("user_permissions")
            .filter(id__in=self.request.user.telegram_users.all(), groups__name=group_name)
            .order_by("last_name", "first_name")
        )
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
