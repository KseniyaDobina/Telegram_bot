import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

# Получение переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')

# URL и эндпойнты к rapidapi.com
API_HOST = 'hotels4.p.rapidapi.com'
RAPID_URL = 'https://' + API_HOST
FIRST_ENDPOINTS = '/locations/v3/search'
SECOND_ENDPOINTS = '/properties/v2/list'
THIRD_ENDPOINTS = '/properties/v2/detail'

LIST_SORT = ('PRICE_LOW_TO_HIGH', 'PRICE_HIGH_TO_LOW', 'DISTANCE')
DEFAULT_COMMANDS = [
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
    ('lowprice', 'Вывести самые дешёвые отели в городе'),
    ('highprice', 'Вывести самые дорогие отели в городе'),
    ('bestdeal', 'Вывести отели, наиболее подходящие по цене и расположению от центра'),
    ('history', 'Вывести историю поиска')
]

HEADERS = {
    'X-RapidAPI-Key': API_KEY,
    'X-RapidAPI-Host': API_HOST,
}
PAYLOAD_HOTEL_DETAIL = {
    "currency": "USD",
    "eapid": 1,
    "locale": "ru_RU",
    "siteId": 300000001
}
