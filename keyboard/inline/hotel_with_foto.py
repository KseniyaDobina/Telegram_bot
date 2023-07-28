from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from states import TownCard


def inline_button_hotels(add_button_hotel):
    """
    Добавляет в inline клавиатуру кнопки для перелистывания отелей
    :param add_button_hotel: inline клавиатуру
    :return: inline клавиатуру
    """
    if len(TownCard.hotel_list) == 1:
        add_button_hotel.add(
            InlineKeyboardButton("✖️",
                                 callback_data="null"),
            InlineKeyboardButton(f"{TownCard.hotel_number + 1} из {len(TownCard.hotel_list)} отелей",
                                 callback_data="null"),
            InlineKeyboardButton("✖️",
                                 callback_data="null"),
        )

    elif TownCard.hotel_number == 0:
        add_button_hotel.add(
            InlineKeyboardButton("✖️",
                                 callback_data="null"),
            InlineKeyboardButton(f"{TownCard.hotel_number + 1} из {len(TownCard.hotel_list)} отелей",
                                 callback_data="null"),
            InlineKeyboardButton("Следующий",
                                 callback_data=f"clickh: {TownCard.hotel_number + 1}"),
        )

    elif TownCard.hotel_number == len(TownCard.hotel_list) - 1:
        add_button_hotel.add(
            InlineKeyboardButton("Предыдущий",
                                 callback_data=f"clickh: {TownCard.hotel_number - 1}"),
            InlineKeyboardButton(f"{TownCard.hotel_number + 1} из {len(TownCard.hotel_list)} отелей",
                                 callback_data="null"),
            InlineKeyboardButton("✖️",
                                 callback_data="null"),
        )

    else:
        add_button_hotel.add(
            InlineKeyboardButton("Предыдущий",
                                 callback_data=f"clickh: {TownCard.hotel_number - 1}"),
            InlineKeyboardButton(f"{TownCard.hotel_number + 1} из {len(TownCard.hotel_list)} отелей",
                                 callback_data="null"),
            InlineKeyboardButton("Следующий",
                                 callback_data=f"clickh: {TownCard.hotel_number + 1}"),
        )
    add_button_hotel.add(
        InlineKeyboardButton("Закончить просмотр",
                             callback_data="end"),
    )

    return add_button_hotel


def inline_button_hotel_with_foto():
    """
    Создает inline клавиатуру.
    :return: inline клавиатуру
    """
    if TownCard.foto == 1:
        inline_keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("✖️️",
                                 callback_data="null"),
            InlineKeyboardButton(f"{TownCard.foto_number + 1} из {TownCard.foto} фото",
                                 callback_data="null"),
            InlineKeyboardButton("✖️",
                                 callback_data="null"),
        )
        inline_keyboard = inline_button_hotels(inline_keyboard)

    elif TownCard.foto_number == 0:
        inline_keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("✖️️",
                                 callback_data="null"),
            InlineKeyboardButton(f"{TownCard.foto_number + 1} из {TownCard.foto} фото",
                                 callback_data="null"),
            InlineKeyboardButton("▶️",
                                 callback_data=f"clickf: {TownCard.foto_number + 1}"),
        )
        inline_keyboard = inline_button_hotels(inline_keyboard)

    elif TownCard.foto_number == TownCard.foto - 1:
        inline_keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("◀️️️",
                                 callback_data=f"clickf: {TownCard.foto_number - 1}"),
            InlineKeyboardButton(f"{TownCard.foto_number + 1} из {TownCard.foto} фото",
                                 callback_data="null"),
            InlineKeyboardButton("✖️",
                                 callback_data="null"),
        )
        inline_keyboard = inline_button_hotels(inline_keyboard)

    else:
        inline_keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("◀",
                                 callback_data=f"clickf: {TownCard.foto_number - 1}"),
            InlineKeyboardButton(f"{TownCard.foto_number + 1} из {TownCard.foto} фото",
                                 callback_data="null"),
            InlineKeyboardButton("▶️",
                                 callback_data=f"clickf: {TownCard.foto_number + 1}"),
        )
        inline_keyboard = inline_button_hotels(inline_keyboard)

    return inline_keyboard
