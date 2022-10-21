from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot):
    """
    Добавляет список команд в бот
    :param bot: бот в телеграмме
    """
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
