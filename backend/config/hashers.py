from passlib.hash import pbkdf2_sha256


def hash_telegram_id(telegram_id):
    # bcrypt.hash(telegram_id)
    h = pbkdf2_sha256.using(salt_size=1).hash(telegram_id)
    return h
