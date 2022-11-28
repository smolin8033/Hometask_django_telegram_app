from passlib.hash import bcrypt


def hash_telegram_id(telegram_id):
    h = bcrypt.hash(telegram_id)
    return h
