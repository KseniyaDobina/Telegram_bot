from telebot.types import Message
from loader import bot
from config_data.config import DEFAULT_COMMANDS


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    """
    Отправляет список всех команд.
    :param message: Сообщение из бота
    """
    list_fun = '\n'.join([f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS])
    text = f"Список всех команд:" \
           f"\n{list_fun}"
    bot.send_message(message.chat.id, text)
