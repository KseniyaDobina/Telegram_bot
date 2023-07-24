import sqlite3 as sq
import datetime
# from .models import User, CommandHistory, Hotel
from peewee import *

db = SqliteDatabase('bot.db')


class GeneralModel(Model):
    class Meta:
        database = db


class User(GeneralModel):
    id_telegram = IntegerField()


class CommandHistory(GeneralModel):
    user = ForeignKeyField(User)
    command = CharField()
    date = DateField(default=datetime.datetime.now())
    town = CharField()


class Hotel(GeneralModel):
    command = ForeignKeyField(CommandHistory)
    name = CharField()
    link = CharField()


def create_tables():
    """
    Создает три таблицы: users, commands_history, hotels.
    """

    tables = [User, CommandHistory, Hotel]
    if not all(table.table_exists() for table in tables):
        db.create_tables(tables)  # создаем таблицы
        print('Таблицы созданы успешно.')
        # logger.debug('Таблицы созданы успешно.')
    else:
        print('Таблицы уже существуют.')
        # logger.debug('Таблицы уже существуют.')


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
        user = User(id_telegram=id_user)
        user.save()
        return user.id


def add_commands(user_id, command, town):
    """
    Добавляет новую команду и город, где производился поиск.
    :param user_id: Id пользователя в базе данных
    :param command: Название команды
    :param town: Город
    :return: id добавленной команды
    """

    new_command = CommandHistory(user=user_id, command=command, town=town)
    new_command.save()
    return new_command.id


def add_hotels(command_id, hotel_name, link):
    """
    Добавляет отель.
    :param command_id: Id команды
    :param hotel_name: Название отеля
    :param link: Ссылка на отель
    """
    new_hotel = Hotel(command=command_id, name=hotel_name, link=link)
    new_hotel.save()


def list_commands(user_id):
    """
    Находит и возвращает список команд, которые вводил пользователь
    :param user_id: id пользователя
    :return: список команд
    """
    with sq.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(f"SELECT commands_history.command_id, commands_history.command, "
                    f"commands_history.date, commands_history.town FROM users "
                    f"JOIN commands_history ON users.user_id = commands_history.user_id "
                    f"WHERE users.user_id={user_id}")
        result = cur.fetchall()
        if result:
            return result
        else:
            return False


def list_hotels(command_id):
    """
    Находит и возвращает список отелей для определенной команды
    :param command_id: id команды
    :return: список отелей
    """
    with sq.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(f"SELECT hotel_name, link FROM hotels WHERE command_id={command_id}")
        return cur.fetchall()
