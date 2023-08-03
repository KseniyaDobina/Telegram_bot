import datetime
import json

from telebot.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton, InputMediaPhoto, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar

from db_sqlite.models import Hotel
from loader import bot
from states import TownCard, UserCard, HotelCard
from config_data import config, parse, hotel_info
from keyboard import inline
from db_sqlite import db_functions


@bot.message_handler(commands=['lowprice'])
def first_question(message: Message):
    """
    Добавляет id пользователя и дату.
    :param message: Сообщение из бота
    """
    UserCard.id = db_functions.check_user(message.from_user.id)
    UserCard.command = 'lowprice'
    UserCard.date_and_time = datetime.datetime.now()
    ask = bot.send_message(message.chat.id, 'В каком городе смотрим отели?')
    bot.register_next_step_handler(ask, find_neighborhood)


@bot.message_handler(commands=['highprice'])
def first_question(message: Message):
    """
    Добавляет id пользователя и дату.
    :param message: Сообщение из бота
    """
    UserCard.id = db_functions.check_user(message.from_user.id)
    UserCard.command = 'highprice'
    UserCard.date_and_time = datetime.datetime.now()
    ask = bot.send_message(message.chat.id, 'В каком городе смотрим отели?')
    bot.register_next_step_handler(ask, find_neighborhood)


@bot.message_handler(commands=['bestdeal'])
def first_question(message: Message):
    """
    Добавляет id пользователя и дату.
    :param message: Сообщение из бота
    """
    UserCard.id = db_functions.check_user(message.from_user.id)
    UserCard.command = 'bestdeal'
    UserCard.date_and_time = datetime.datetime.now()
    ask = bot.send_message(message.chat.id, 'В каком городе смотрим отели?')
    bot.register_next_step_handler(ask, find_neighborhood)


def find_neighborhood(message: Message):
    """
    Находит районы города и выводит inline клавиатуру.
    :param message: Сообщение из бота
    """
    answer = message.text.lower()
    TownCard.town = answer
    querystring = {'q': TownCard.town, 'locale': 'ru_RU', 'currency': 'USD', "siteid": "300000001"}
    data = parse.request_to_api(url=config.RAPID_URL + config.FIRST_ENDPOINTS,
                                headers=config.HEADERS,
                                params=querystring)
    neighborhood = {}
    try:
        if len(data['sr']) == 0:
            raise KeyError
        for region in data['sr']:
            if not region['regionNames']['shortName'] in neighborhood.values():
                neighborhood[region['gaiaId']] = region['regionNames']['shortName']
        TownCard.list_key = neighborhood
        destinations = InlineKeyboardMarkup()
        for id_city in neighborhood.keys():
            destinations.add(InlineKeyboardButton(text=neighborhood[id_city], callback_data=id_city))
        bot.send_message(message.from_user.id, 'Уточните, пожалуйста:', reply_markup=destinations)
    except KeyError:
        with open('tests/errors_list_town.json', 'w') as f:
            json.dump(data, f)
        ask = bot.send_message(message.chat.id, 'Я не могу найти отели в этом городе, пожалуйста введите другой.')
        bot.register_next_step_handler(ask, find_neighborhood)
    except TypeError:
        ask = bot.send_message(message.chat.id, 'Я не могу найти отели в этом городе, пожалуйста введите другой или '
                                                'попробуйте ввести название города иначе.')
        bot.register_next_step_handler(ask, find_neighborhood)


@bot.callback_query_handler(func=lambda call: call.data in TownCard.list_key.keys())
def find_destination_id(call: CallbackQuery):
    """
    Сохраняет выбранный район.
    :param call: Сообщение из бота
    """
    answer = call.data
    TownCard.destination_id = answer
    bot.edit_message_text(f'Вы выбрали {TownCard.list_key[answer]}',
                          call.message.chat.id,
                          call.message.message_id)
    if parse.sort_hotels(UserCard.command) == 'DISTANCE':
        ask = bot.send_message(call.message.chat.id, 'Введите минимальную стоимость в сутки')
        bot.register_next_step_handler(ask, min_price)
    else:
        bot.send_message(call.message.chat.id, 'Выберите дату, когда Вы въедете в отель')
        TownCard.min_date = datetime.date.today()
        calendar, step = DetailedTelegramCalendar(locale='ru', min_date=TownCard.min_date).build()
        bot.send_message(call.message.chat.id,
                         'Выберите год',
                         reply_markup=calendar)


def min_price(message: Message):
    """
    Сохраняет минимальную стоимость.
    :param message: Сообщение из бота
    """
    answer = message.text
    if answer.isdigit():
        if int(answer) < 0:
            ask = bot.send_message(message.chat.id, 'Минимальная стоимость должна быть больше нуля.')
            bot.register_next_step_handler(ask, min_price)
        else:
            TownCard.min_price = int(answer)
            ask = bot.send_message(message.chat.id, 'Введите максимальную стоимость в сутки')
            bot.register_next_step_handler(ask, max_price)
    else:
        ask = bot.send_message(message.chat.id, 'Минимальная стоимость в сутки должна быть числом')
        bot.register_next_step_handler(ask, min_price)


def max_price(message: Message):
    """
    Сохраняет максимальную стоимость.
    :param message: Сообщение из бота
    """
    answer = message.text
    if answer.isdigit():
        if int(answer) <= int(TownCard.min_price):
            ask = bot.send_message(message.chat.id, 'Максимальная цена должна быть больше минимальной.')
            bot.register_next_step_handler(ask, max_price)
        else:
            TownCard.max_price = int(answer)
            ask = bot.send_message(message.chat.id, 'Введите максимальное расстояние до центра')
            bot.register_next_step_handler(ask, max_landmark)
    else:
        ask = bot.send_message(message.chat.id, 'Максимальная цена должна быть числом.')
        bot.register_next_step_handler(ask, max_price)


def max_landmark(message: Message):
    """
    Сохраняет максимальное расстояние до центра.
    :param message: Сообщение из бота
    """
    answer = message.text
    if answer.isdigit():
        if float(answer) < 0:
            ask = bot.send_message(message.chat.id, 'Максимальное расстояние не может быть отрицательным.'
                                                    ' Пожалуйста введите максимальное расстояние ещё раз')
            bot.register_next_step_handler(ask, max_landmark)
        else:
            TownCard.max_landmark = float(answer)
            TownCard.min_date = datetime.date.today()
            calendar, step = DetailedTelegramCalendar(locale='ru', min_date=TownCard.min_date).build()
            bot.send_message(message.chat.id, 'Выберите год', reply_markup=calendar)
    else:
        ask = bot.send_message(message.chat.id, 'Максимальное расстояние должно быть числом.')
        bot.register_next_step_handler(ask, max_landmark)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def callback_calendar(callback: CallbackQuery):
    """
    Сохраняет дату въезда и выезда.
    :param callback: Сообщение из бота
    """
    lstep = {'y': 'год', 'm': 'месяц', 'd': 'день'}
    result, key, step = DetailedTelegramCalendar(locale='ru', min_date=TownCard.min_date).process(callback.data)
    if not result and key:
        bot.edit_message_text(f'Выберите {lstep[step]}',
                              callback.message.chat.id,
                              callback.message.message_id,
                              reply_markup=key)
    elif result:
        if TownCard.from_date_control != 1:
            TownCard.from_date_control = 1
            bot.edit_message_text(f'Выбранная дата въезда {result}',
                                  callback.message.chat.id,
                                  callback.message.message_id)
            bot.send_message(callback.message.chat.id, 'Выберите дату, когда Вы будете выезжать из отеля')
            TownCard.from_date = result
            TownCard.min_date = TownCard.from_date + datetime.timedelta(days=1)
            calendar, step = DetailedTelegramCalendar(locale='ru', min_date=TownCard.min_date).build()
            bot.send_message(callback.message.chat.id, f'Выберите {lstep[step]}', reply_markup=calendar)
        else:
            bot.edit_message_text(f'Выбранная дата выезда {result}',
                                  callback.message.chat.id,
                                  callback.message.message_id)
            TownCard.to_date = result
            TownCard.from_date_control = 0
            reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
            reply_markup.row('Да ✅', 'Нет ❌')
            ask = bot.send_message(callback.from_user.id, 'Вам нужны фото отелей?', reply_markup=reply_markup)
            bot.register_next_step_handler(ask, check_foto)


def check_foto(message: Message):
    """
    Запрашивает количество фото.
    :param message: Сообщение из бота
    """
    answer = message.text
    if answer == "Да ✅":
        TownCard.foto = 5
        ask = bot.send_message(message.chat.id, "Сколько Вы хотите фото отеля (максимум 5)",
                               reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(ask, number_of_foto)
    elif answer == 'Нет ❌':
        TownCard.foto = 0
        ask = bot.send_message(message.chat.id, "Сколько Вы хотите видеть отелей (максимум 25)",
                               reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(ask, find_hotels)
    else:
        reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
        reply_markup.row('Да ✅', 'Нет ❌')
        ask = bot.send_message(message.chat.id, "Пожалуйста выберите из кнопок ниже", reply_markup=reply_markup)
        bot.register_next_step_handler(ask, check_foto)


def number_of_foto(message: Message):
    """
    Сохраняет количество фото.
    :param message: Сообщение из бота
    """
    if message.text.isdigit():
        answer = int(message.text)
        if answer < 1:
            ask = bot.send_message(message.chat.id, "Вы ввели количество меньше 1,"
                                                    " чтобы увидеть фотографии отеля,"
                                                    " нужно ввести число больше или равное 1")
            bot.register_next_step_handler(ask, number_of_foto)
        elif answer > 5:
            ask = bot.send_message(message.chat.id, "Я могу вывести максимум пять фото, пожалуйста введите число"
                                                    " меньше")
            bot.register_next_step_handler(ask, number_of_foto)
        else:
            TownCard.foto = answer
            ask = bot.send_message(message.chat.id, "Сколько Вы хотите видеть отелей (максимум 25)?")
            bot.register_next_step_handler(ask, find_hotels)
    else:
        ask = bot.send_message(message.chat.id, "Количество фото должно быть числом от 1 до 5.")
        bot.register_next_step_handler(ask, number_of_foto)


def find_hotels(message: Message):
    """
    Находит отели по всем запросам и выводит их.
    :param message: Сообщение из бота
    """
    if message.text.isdigit():
        answer = message.text
        if int(answer) < 1:
            ask = bot.send_message(message.chat.id, "Я не могу вывести меньше одного отеля,"
                                                    " введите число больше или равное 1")
            bot.register_next_step_handler(ask, find_hotels)
        elif int(answer) > 25:
            TownCard.foto = answer
            ask = bot.send_message(message.chat.id, "Я могу вывести максимум 25 отелей, пожалуйста введите число "
                                                    "меньше")
            bot.register_next_step_handler(ask, find_hotels)
        else:
            bot.send_message(message.chat.id, "Подождите, идёт загрузка", reply_markup=ReplyKeyboardRemove())
            in_date = TownCard.from_date
            out_date = TownCard.to_date
            payload = {
                "currency": "USD",
                "eapid": 1,
                "locale": "ru_RU",
                "siteId": 300000001,
                "destination": {"regionId": str(TownCard.destination_id)},
                "checkInDate": {
                    "day": int(in_date.day),
                    "month": int(in_date.month),
                    "year": int(in_date.year)
                },
                "checkOutDate": {
                    "day": int(out_date.day),
                    "month": int(out_date.month),
                    "year": int(out_date.year)
                },
                "rooms": [{"adults": 1}],
                "resultsStartingIndex": 0,
                "resultsSize": int(answer),
                "sort": parse.sort_hotels(UserCard.command),
                "filters": {"availableFilter": "SHOW_AVAILABLE_ONLY"}
                # "filters": {"price": {
                #     "max": 150,
                #     "min": 100
                # }}
            }
            if type(TownCard.max_price) == int and type(TownCard.min_price) == int:
                if TownCard.min_price == 0:
                    TownCard.min_price = 1
                payload["filters"] = {"price": {"min": TownCard.min_price, "max": TownCard.max_price},
                                      "availableFilter": "SHOW_AVAILABLE_ONLY"}
            try:
                answer = parse.request_to_api(url=config.RAPID_URL + config.SECOND_ENDPOINTS,
                                              headers=config.HEADERS,
                                              params=payload,
                                              post=True)
                TownCard.hotel_list = answer["data"]["propertySearch"]["properties"]
                if parse.sort_hotels(UserCard.command) == config.LIST_SORT[2]:
                    TownCard.hotel_list = parse.check_centre(TownCard.hotel_list)
                if len(TownCard.hotel_list) == 0:
                    print('Нет отелей')
                    raise KeyError
                TownCard.hotel_number = 0
                days = TownCard.to_date - TownCard.from_date
                payload = config.PAYLOAD_HOTEL_DETAIL
                payload['propertyId'] = str(TownCard.hotel_list[0]['id'])
                answer = parse.request_to_api(url=config.RAPID_URL + config.THIRD_ENDPOINTS, headers=config.HEADERS,
                                              params=payload, post=True)
                price, text = hotel_info.get_info_about_hotel(TownCard.hotel_list[0],
                                                              answer['data']['propertyInfo']['summary'],
                                                              days)
                HotelCard.hotel_text = text
                if not TownCard.foto:
                    markup = inline.inline_hotel_without_foto()
                    bot.send_message(message.chat.id, 'Выберите отель')
                    bot.send_message(message.chat.id, text, reply_markup=markup)
                else:
                    TownCard.foto_number = 0
                    markup = inline.inline_button_hotel_with_foto()
                    TownCard.foto_list = hotel_info.get_foto(
                        answer['data']['propertyInfo']['propertyGallery']['images'],
                        TownCard.foto)
                    bot.send_message(message.chat.id, 'Выберите отель')
                    bot.send_photo(message.chat.id, TownCard.foto_list[0], caption=text, reply_markup=markup)
            except KeyError:
                with open('tests/errors.json', 'w') as f:
                    json.dump(answer, f)
                bot.send_message(message.chat.id, 'К сожалению, я не смог найти отели')
            except TypeError:
                bot.send_message(message.chat.id, 'К сожалению, возникли ошибки на сервисе. Попробуйте ещё раз')
    else:
        ask = bot.send_message(message.chat.id, "Количество отелей должно быть числом от 1 до 25")
        bot.register_next_step_handler(ask, find_hotels)


@bot.callback_query_handler(func=lambda call: call.data.startswith("click"))
def inline_keyboard_answer(call: CallbackQuery):
    """
    Выводит отели.
    :param call: Сообщение из бота
    """
    days = TownCard.to_date - TownCard.from_date
    if call.data.startswith("clickwf"):
        TownCard.hotel_number = int(call.data.split()[1])
        payload = config.PAYLOAD_HOTEL_DETAIL
        payload['propertyId'] = str(TownCard.hotel_list[TownCard.hotel_number]['id'])
        answer = parse.request_to_api(url=config.RAPID_URL + config.THIRD_ENDPOINTS, headers=config.HEADERS,
                                      params=payload, post=True)
        price, text = hotel_info.get_info_about_hotel(TownCard.hotel_list[0],
                                                      answer['data']['propertyInfo']['summary'],
                                                      days)
        HotelCard.hotel_text = text
        markup = inline.inline_hotel_without_foto()
        bot.edit_message_text(HotelCard.hotel_text, call.message.chat.id, call.message.message_id, reply_markup=markup)
    else:
        if call.data.startswith("clickh"):
            TownCard.hotel_number = int(call.data.split()[1])
            payload = config.PAYLOAD_HOTEL_DETAIL
            payload['propertyId'] = str(TownCard.hotel_list[TownCard.hotel_number]['id'])
            answer = parse.request_to_api(url=config.RAPID_URL + config.THIRD_ENDPOINTS, headers=config.HEADERS,
                                          params=payload, post=True)
            price, text = hotel_info.get_info_about_hotel(
                TownCard.hotel_list[TownCard.hotel_number],
                answer['data']['propertyInfo']['summary'],
                days)
            HotelCard.hotel_text = text
            TownCard.foto_list = hotel_info.get_foto(
                answer['data']['propertyInfo']['propertyGallery']['images'],
                TownCard.foto)
            TownCard.foto_number = 0

        elif call.data.startswith("clickf"):
            TownCard.foto_number = int(call.data.split()[1])
        markup = inline.inline_button_hotel_with_foto()
        media = InputMediaPhoto(TownCard.foto_list[TownCard.foto_number],
                                caption=HotelCard.hotel_text)
        bot.edit_message_media(media, call.message.chat.id, call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'end')
def saving_history(call: CallbackQuery):
    """
    Сохраняет в базу данных команду и отели.
    :param call: Сообщение из бота
    """
    new_command_id = db_functions.add_commands(UserCard.id, UserCard.command, TownCard.town)
    days = TownCard.to_date - TownCard.from_date
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, f"Последний просмотренный отель:")
    if TownCard.foto != 0:
        all_foto = [InputMediaPhoto(TownCard.foto_list[0], caption=HotelCard.hotel_text)]
        for id_foto in range(1, len(TownCard.foto_list)):
            all_foto.append(InputMediaPhoto(TownCard.foto_list[id_foto]))
        bot.send_media_group(call.message.chat.id, all_foto)
    else:
        bot.send_message(call.message.chat.id, HotelCard.hotel_text)
    for hotel_count in TownCard.hotel_list:
        Hotel.create(command=new_command_id, name=hotel_count['name'],
                     link=f"hotels.com/h{hotel_count['id']}.Hotel-Information")
