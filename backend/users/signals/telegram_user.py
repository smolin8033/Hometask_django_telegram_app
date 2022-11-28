# flake8: noqa
from django.db.models.signals import pre_save
from django.dispatch import receiver

from config.loggers import logger
from users.models import TelegramUser


@receiver(pre_save, sender=TelegramUser)
def telegram_user_pre_save(sender, instance, *args, **kwargs):
    instance.telegram_id = "something"
