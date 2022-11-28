from rest_framework.serializers import ModelSerializer

from users.models import TelegramUser


class TelegramUserSerializer(ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = "__all__"
