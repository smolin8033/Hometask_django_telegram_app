from typing import Callable

from rest_framework.request import Request
from rest_framework.response import Response

from config.hashers import myctx
from users.models import TelegramUser


class CheckAuthorization:
    def __init__(self, get_response: Callable) -> None:
        """One-time configuration and initialization."""
        self.get_response = get_response

    def __call__(self, request: Request) -> Response:
        """
        Code to be executed for each request before
        the view (and later middleware) are called.
        """
        if "Username" in request.headers:
            try:

                telegram_user = TelegramUser.objects.get(username=request.headers.get("Username"))

                if myctx.verify(request.headers.get("Telegram-Id"), telegram_user.telegram_id):
                    request.user = telegram_user

            except TelegramUser.DoesNotExist:
                ...

        response = self.get_response(request)

        return response
