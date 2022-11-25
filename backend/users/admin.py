from django.contrib import admin

from users.models import TelegramUser, User


@admin.register(User)
class User(admin.ModelAdmin):
    pass


@admin.register(TelegramUser)
class TelegramUser(admin.ModelAdmin):
    pass
