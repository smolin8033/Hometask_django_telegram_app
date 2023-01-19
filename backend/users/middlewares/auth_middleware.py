from django.utils.deprecation import MiddlewareMixin
from passlib.hash import pbkdf2_sha256

# from config.hashers import hash_telegram_id
from config.loggers import logger
from users.models import TelegramUser


class CheckAuthorization(MiddlewareMixin):
    def process_request(self, request):
        """
        три условия:
        - не в бд и в хедерах нет роли кидать 422 ошибку (мб 401) не делаю пока

        - пользователь есть в бд, засунуть в реквест юзер
        - есть в хедере роль и пользователя нет в бд просто дальше
        """
        try:
            logger.critical(request.headers)

            telegram_user = TelegramUser.objects.get(username=request.headers.get("Username"))
            # logger.error(telegram_user.telegram_id)
            # logger.error(hash_telegram_id(request.headers.get("Telegram-Id")))
            logger.error(
                f"Verification {pbkdf2_sha256.verify(request.headers.get('Telegram-Id'), telegram_user.telegram_id)}"
            )
            # request.user = telegram_user

        except TelegramUser.DoesNotExist:
            logger.info("Unsuccessful")
            telegram_user = None

            return telegram_user
