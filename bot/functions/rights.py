from functools import wraps

from aiogram import types


admin_list = [626591599, 342120556]
users = []
secret_words = ['рахмет']


def is_Admin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        message: types.Message = args[0]
        if message.from_user.id in admin_list:
            return await func(*args, **kwargs)
    return wrapper


def is_admin(user_id):
    return True if user_id in admin_list else False


def is_User(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        message: types.Message = args[0]
        if message.from_user.id in users:
            return await func(*args, **kwargs)
    return wrapper


def is_user(user_id):
    return True if user_id in users else False
