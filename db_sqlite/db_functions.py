# from .models import User, CommandHistory, Hotel
from .models import User, Hotel


def check_user(id_user):
    """
    Проверяет наличие пользователя в базе данных. При отсутствии пользователя в бд, добавляет его.
    При наличии возвращает id пользователя в бд.
    :param id_user: Id пользователя в телеграмме
    :return: присвоенный пользователю id
    """
    try:
        user = User.get(User.id_telegram == id_user)
        return user.id
    except User.DoesNotExist:
        user = User.create(id_telegram=id_user)
        return user.id
