from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Пользователь телеграма
    """

    telegram_id = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]
