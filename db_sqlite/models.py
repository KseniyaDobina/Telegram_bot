import datetime
from peewee import *

from .settings import db


def create_tables():
    """
    Создает три таблицы: users, commands_history, hotels.
    """

    tables = [User, Hotel]
    if not all(table.table_exists() for table in tables):
        db.create_tables(tables)  # создаем таблицы
        print('Таблицы созданы успешно.')
        # logger.debug('Таблицы созданы успешно.')
    else:
        print('Таблицы уже существуют.')
        # logger.debug('Таблицы уже существуют.')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id_telegram = IntegerField()

    class Meta:
        table_name = 'users'


class Hotel(BaseModel):
    id_in_API = IntegerField()
    user = ForeignKeyField(User)
    command = CharField()
    date = DateField(default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    town = CharField()
    name = CharField()
    link = CharField()
    price = IntegerField()
    favorite = BooleanField(default=False)
    history = BooleanField(default=True)

    class Meta:
        table_name = 'hotels'
