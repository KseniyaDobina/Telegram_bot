from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from states import TownCard


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
            InlineKeyboardButton("Следующий️",
                                 callback_data=f"clickwf: {TownCard.hotel_number + 1}"),
        )

    elif TownCard.hotel_number == len(TownCard.hotel_list) - 1:
        inline_keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Предыдущий️",
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

    inline_keyboard.add(
        InlineKeyboardButton("Закончить просмотр",
                             callback_data="end"),
    )
    return inline_keyboard
