from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
from db import db

if __name__ == '__main__':
    db.create_tables()
    set_default_commands(bot)
    bot.infinity_polling()
