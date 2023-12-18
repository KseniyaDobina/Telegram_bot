from telebot.handler_backends import State, StatesGroup


class TownCard(StatesGroup):
    """
    Класс города, в котором происходит поиск информации
    Атрибуты:
        town: город
        list_key: список id районов в городе
        destination_id: id района в городе
        min_price: минимальная цена
        max_price: максимальная цена
        max_landmark: максимальное расстояние до центра
        min_date: дата, для контроля функции календаря
        from_date: дата въезда
        from_date_control: контроль за выбором даты из календаря
        to_date: дата выезда
        hotel_list: список отелей
        hotel_number: id просматриваемого отеля
        foto: количество фото
        foto_list: список фото
        foto_number: id просматриваемого фото
    """
    town = State()
    list_key = []
    destination_id = State()
    min_price = State()
    max_price = State()
    max_landmark = State()
    foto = State()
    min_date = State()
    from_date = State()
    from_date_control = State()
    to_date = State()
    hotel_list = State()
    hotel_number = State()
    foto_number = State()
    foto_list = State()


class HotelCard(StatesGroup):
    id_in_API = State()
    hotel_text = State()
    price = State()
    # foto_list = State()


class UserCard(StatesGroup):
    """
    Класс Пользователя
    Атрибуты:
        id: id пользователя
        command: введенная команда
        date_and_time: дата и время, когда была введена команда
    """
    id = State()
    command = State()
