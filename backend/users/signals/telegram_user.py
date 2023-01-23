# flake8: noqa
from django.db.models.signals import pre_save
from django.dispatch import receiver

from config.hashers import hash_telegram_id
from users.models import TelegramUser


@receiver(pre_save, sender=TelegramUser)
def telegram_user_pre_save(sender, instance, *args, **kwargs):
    if instance.id is None:
        instance.telegram_id = hash_telegram_id(instance.telegram_id)
