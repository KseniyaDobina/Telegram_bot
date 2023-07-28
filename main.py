from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
from db_sqlite import models

if __name__ == '__main__':
    models.create_tables()
    set_default_commands(bot)
    bot.infinity_polling()
