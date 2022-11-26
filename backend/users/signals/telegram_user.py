from django.db.models.signals import pre_save

from users.serializers import TelegramUserSerializer


def telegram_user_pre_save(sender, instance, *args, **kwargs):
    pass


pre_save.connect(telegram_user_pre_save, sender=TelegramUserSerializer)
