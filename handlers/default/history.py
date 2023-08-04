from telebot.types import Message

from db_sqlite import db_functions
from db_sqlite.models import CommandHistory, Hotel
from loader import bot
from states import UserCard


@bot.message_handler(commands=['history'])
def bot_start(message: Message):
    """
    Отправляет историю поиска отелей.
    :param message: Сообщение из бота
    """
    UserCard.id = db_functions.check_user(message.from_user.id)
    history = db_functions.list_commands(UserCard.id)
    nn = '\n\n'
    tt = '\t\t\t\t'
    if history:
        history_text = '*История запросов:*'
        for command_id in history:
            command = CommandHistory.get(id=command_id)
            history_text += f"{nn}*Команда: /{command.command}\nДата и время ввода команды: {command.date}*" \
                            f"\nГород, в котором производился поиск: {command.town}"

            # count = 0
            #
            # for id_hotel in Hotel.filter(command=command_id):
            #     if count == 4:
            #         break
            #     hotel = Hotel.get(id=id_hotel)
            #     history_text += f"{nn}{tt}{hotel.id}) Название отеля: {hotel.name}" \
            #                     f"\n{tt}Ссылка на отель: {hotel.link}"
            #     count += 1

        bot.send_message(message.chat.id, history_text, parse_mode='Markdown')

    else:
        bot.send_message(message.chat.id, f"История пуста")
