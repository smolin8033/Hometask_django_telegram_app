from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    """
    Модель для админа. У него может быть телеграм id по желанию
    """

    telegram_id = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]

    class Meta:
        verbose_name = "Суперъюзер"
        verbose_name_plural = "Суперъюзеры"


class TelegramUser(AbstractUser):
    """
    Модель пользователей Telegram
    """

    telegram_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=True)
    password = None
    telegram_users = models.ManyToManyField("self", blank=True, related_name="users")

    USERNAME_FIELD = "username"

    groups = models.ManyToManyField(
        Group,
        verbose_name=("telegram_groups"),
        blank=True,
        help_text=(
            "The groups this telegram user belongs to. A telegram user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="telegram_user_set",
        related_query_name="telegram_user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=("telegram user permissions"),
        blank=True,
        help_text=("Specific permissions for this telegram user."),
        related_name="telegram_user_set",
        related_query_name="telegram_user",
    )

    class Meta:
        verbose_name = "Пользователь телеграма"
        verbose_name_plural = "Пользователи телеграма"

    def __str__(self) -> str:
        return "{} {}".format(self.first_name, self.last_name)
