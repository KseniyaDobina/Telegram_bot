from .models import User, CommandHistory, Hotel


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


def add_commands(user_id, command, town):
    """
    Добавляет новую команду и город, где производился поиск.
    :param user_id: Id пользователя в базе данных
    :param command: Название команды
    :param town: Город
    :return: id добавленной команды
    """

    new_command = CommandHistory.create(user=user_id, command=command, town=town)
    return new_command.id


def list_commands(user_id):
    """
    Находит и возвращает список команд, которые вводил пользователь
    :param user_id: id пользователя
    :return: список команд
    """
    try:
        commands = CommandHistory.filter(user=user_id)
        return commands
    except CommandHistory.DoesNotExist:
        return False
