from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния

@bot.message_handler(state=None)
def bot_echo(message: Message):
    """
        Отправляет сообщение пользователю.
        :param message: Сообщение из бота
        """
    if message.text.lower().strip() == 'привет':
        bot.send_message(message.chat.id, f"Привет, {message.from_user.full_name}."
                                          f"\nЧтобы использовать бота, вам нужно выбрать команду."
                                          f"\nВоспользуйтесь /help, чтобы посмотреть список команд.")
    else:
        bot.send_message(message.chat.id, "Я не понимаю, что Вы хотите. "
                                          "Воспользуйтесь /help, чтобы посмотреть список команд.")
