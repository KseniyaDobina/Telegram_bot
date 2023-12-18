from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from db_sqlite.models import Hotel
from states import TownCard, UserCard, HotelCard


def inline_hotel_without_foto():
    """
        Создает inline клавиатуру.
        :return: inline клавиатуру
        """
    if len(TownCard.hotel_list) == 1:
        inline_keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("✖️",
                                 callback_data="null"),
            InlineKeyboardButton(f"{TownCard.hotel_number + 1} из {len(TownCard.hotel_list)} отелей",
                                 callback_data="null"),
            InlineKeyboardButton("✖️",
                                 callback_data="null"),
        )

    elif TownCard.hotel_number == 0:
        inline_keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("✖️",
                                 callback_data="null"),
            InlineKeyboardButton(f"{TownCard.hotel_number + 1} из {len(TownCard.hotel_list)} отелей",
                                 callback_data="null"),
            InlineKeyboardButton("Следующий",
                                 callback_data=f"clickwf: {TownCard.hotel_number + 1}"),
        )

    elif TownCard.hotel_number == len(TownCard.hotel_list) - 1:
        inline_keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Предыдущий",
                                 callback_data=f"clickwf: {TownCard.hotel_number - 1}"),
            InlineKeyboardButton(f"{TownCard.hotel_number + 1} из {len(TownCard.hotel_list)} отелей",
                                 callback_data="null"),
            InlineKeyboardButton("✖️",
                                 callback_data="null"),
        )

    else:
        inline_keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Предыдущий",
                                 callback_data=f"clickwf: {TownCard.hotel_number - 1}"),
            InlineKeyboardButton(f"{TownCard.hotel_number + 1} из {len(TownCard.hotel_list)} отелей",
                                 callback_data="null"),
            InlineKeyboardButton("Следующий",
                                 callback_data=f"clickwf: {TownCard.hotel_number + 1}"),
        )
    if isinstance(TownCard.hotel_list[TownCard.hotel_number], dict):
        if Hotel.select().where(
                Hotel.id_in_API == TownCard.hotel_list[TownCard.hotel_number]['id'],
                Hotel.user == UserCard.id, Hotel.favorite == True).exists():
            inline_keyboard.add(
                InlineKeyboardButton("Удалить из избранного",
                                     callback_data=f"favd: {TownCard.hotel_list[TownCard.hotel_number]['id']}"),
            )
        else:
            inline_keyboard.add(
                InlineKeyboardButton("Добавить в избранное",
                                     callback_data=f"favc: {TownCard.hotel_list[TownCard.hotel_number]['id']}"),
            )
    else:
        if Hotel.select().where(
                Hotel.id_in_API == TownCard.hotel_list[TownCard.hotel_number].id_in_API,
                Hotel.user == UserCard.id).exists():
            hotel = Hotel.get(id_in_API=TownCard.hotel_list[TownCard.hotel_number].id_in_API,user=UserCard.id)
            if hotel.favorite:
                print('78', TownCard.hotel_list[TownCard.hotel_number].id_in_API)
                inline_keyboard.add(
                    InlineKeyboardButton("Удалить из избранного",
                                         callback_data=f"favd: {TownCard.hotel_list[TownCard.hotel_number].id_in_API}"),
                )
            else:
                print('here')
                inline_keyboard.add(
                    InlineKeyboardButton("Добавить в избранное",
                                         callback_data=f"favc: {TownCard.hotel_list[TownCard.hotel_number].id_in_API}"),
                )

    inline_keyboard.add(
        InlineKeyboardButton("Закончить просмотр",
                             callback_data="end"),
    )
    return inline_keyboard
