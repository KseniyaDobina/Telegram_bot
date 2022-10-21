import sqlite3 as sq


def create_tables():
    """
    Создает три таблицы: users, commands_history, hotels.
    """
    with sq.connect('base.db') as db:
        db.execute("PRAGMA foreign_keys = 1")
        cur = db.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                id_telegram INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES commands_history(user_id)
                )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS commands_history (
                user_id INTEGER NOT NULL,
                command_id INTEGER PRIMARY KEY, 
                command TEXT NOT NULL,
                date INTEGER NOT NULL,
                town TEXT NOT NULL,
                FOREIGN KEY (command_id) REFERENCES hotels(command_id)
                )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS hotels (
                command_id INTEGER,
                hotel_name TEXT NOT NULL,
                link TEXT NOT NULL
                )""")


def delete_tables():
    """
    Удаляет все таблицы.
    """
    with sq.connect('base.db') as db:
        cur = db.cursor()
        cur.execute("DROP TABLE users")
        cur.execute("DROP TABLE commands_history")
        cur.execute("DROP TABLE hotels")


def check_user(id_user):
    """
    Проверяет наличие пользователя в базе данных. При отсутвии пользователя в бд, добавляет его.
    При наличии возвращает id пользователя в бд.
    :param id_user: id пользователя в телеграмме
    :return: присвоенный пользователю id
    """
    with sq.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(f"SELECT user_id FROM users WHERE id_telegram = {id_user}")
        find_user = cur.fetchall()
        if find_user:
            for id_count in find_user:
                return id_count[0]

        else:
            cur.execute(f"INSERT INTO users ('user_id', 'id_telegram')"
                        f" VALUES((SELECT max(user_id) FROM users) + 1, {id_user})")
            cur.execute(f"SELECT user_id FROM users WHERE id_telegram = {id_user}")
            for id_count in cur.fetchall():
                return id_count[0]


def add_commands(user_id, command, date, town):
    """
    Добавляет новую команду, а также дату с временем, когда была введена команда, и город, где производился поиск.
    :param user_id: id пользователя в базе данных
    :param command: Название команды
    :param date: Дата и время
    :param town: Город
    :return: id добавленной команды
    """
    with sq.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(f"SELECT max(command_id) FROM commands_history")
        for count in cur.fetchall():
            if count[0]:
                id_count = count[0]

            else:
                id_count = 0

        cur.execute(f"INSERT INTO commands_history ('user_id', 'command_id', 'command', 'date', 'town')"
                    f" VALUES({user_id}, {id_count} + 1, '{command}', '{date}', '{town}')")
        return id_count + 1


def add_hotels(command_id, hotel_name, link):
    """
    Добавляет отель.
    :param command_id: id команды
    :param hotel_name: Название отеля
    :param link: Ссылка на отель
    """
    with sq.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(f"INSERT INTO hotels ('command_id', 'hotel_name', 'link') "
                    f"VALUES({command_id}, '{hotel_name}', '{link}')")


def list_commands(user_id):
    """
    Находит и возвращает список команд, которые вводил пользователь
    :param user_id: id пользователя
    :return: список команд
    """
    with sq.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(f"SELECT commands_history.command_id, commands_history.command, "
                    f"commands_history.date, commands_history.town FROM users "
                    f"JOIN commands_history ON users.user_id = commands_history.user_id "
                    f"WHERE users.user_id={user_id}")
        result = cur.fetchall()
        if result:
            return result
        else:
            return False


def list_hotels(command_id):
    """
    Находит и возвращает список отелей для определенной команды
    :param command_id: id команды
    :return: список отелей
    """
    with sq.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(f"SELECT hotel_name, link FROM hotels WHERE command_id={command_id}")
        return cur.fetchall()
