from telebot.types import Message

from db_sqlite import db_functions
from db_sqlite.models import Hotel
from loader import bot
from states import UserCard


@bot.message_handler(commands=['history'])
def bot_start(message: Message):
    """
    Отправляет историю поиска отелей.
    :param message: Сообщение из бота
    """
    UserCard.id = db_functions.check_user(message.from_user.id)
    history = Hotel.select().where(Hotel.user == UserCard.id).exists()
    # history = CommandHistory.select().where(CommandHistory.user == UserCard.id).exists()
    n = '\n'
    t = '\t' * 6
    if history:
        history_text = '*История запросов:*'
        history = Hotel.filter(user=UserCard.id)
        for number_hotel, hotel in enumerate(history):
            history_text += f"{n * 2} {number_hotel + 1}) *Отель: {hotel.name}*" \
                            f"{n}{t}Цена в сутки: " \
                            f"*{hotel.price if hotel.price else 'Посмотрите актуальную цену на сайте отеля'}$*" \
                            f"{n}{t}Дата и время ввода добавления: *{hotel.date}*" \
                            f"{n}{t}Ссылка отеля: *{hotel.link}*" \
                            f"{n}{t}Город, в котором производился поиск: *{hotel.town}*" \
                            f"{n}{t}*Команда:* /{hotel.command}"

        bot.send_message(message.chat.id, history_text, parse_mode='Markdown')

    else:
        bot.send_message(message.chat.id, f"История пуста")
