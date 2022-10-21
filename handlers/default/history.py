from telebot.types import Message

from loader import bot
from db import db
from states import UserCard


@bot.message_handler(commands=['history'])
def bot_start(message: Message):
    """
    Отправляет историю поиска отелей.
    :param message: сообщение из бота
    """
    UserCard.id = db.check_user(message.from_user.id)
    history = db.list_commands(UserCard.id)
    if history:
        history_text = '*История запросов:*'
        for i in history:
            history_text += f"\n\n*Команда: {i[1]}\nДата и время ввода команды: {i[2]}*" \
                           f"\nГород, в котором произодился поиск: {i[3]}"
            for id_count, hotel in enumerate(db.list_hotels(i[0])):
                history_text += f"\n\n\t\t\t\t{id_count + 1}) Название отеля: {hotel[0]}" \
                                f"\n\t\t\t\tСсылка на отель: {hotel[1]}"

        bot.send_message(message.chat.id, history_text, parse_mode='Markdown')

    else:
        bot.send_message(message.chat.id, f"История пуста")
