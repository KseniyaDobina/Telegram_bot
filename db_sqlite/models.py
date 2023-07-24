import datetime
from .base import BaseModel
from peewee import *


class User(BaseModel):
    id_telegram = IntegerField()


class CommandHistory(BaseModel):
    user = ForeignKeyField(User)
    command = CharField()
    date = DateField(default=datetime.datetime.now().strftime("%Y-%m-%d %H.%M"))
    town = CharField()


class Hotel(BaseModel):
    command = ForeignKeyField(CommandHistory)
    name = CharField()
    link = CharField()
