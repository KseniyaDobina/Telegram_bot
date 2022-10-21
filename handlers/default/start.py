from telebot.types import Message
from loader import bot
from db import db
from states import UserCard


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    """
    Отправляет сообщение приветствия пользователю.
    :param message: сообщение из бота
    """
    db.check_user(message.from_user.id)
    UserCard.id = message.from_user.id
    bot.send_message(message.chat.id, f"Привет, {message.from_user.full_name}!"
                                      f"\nЧтобы использовать бота, вам нужно выбрать команду."
                                      f"\nВоспользуйтесь /help, чтобы посмотреть список команд.")
