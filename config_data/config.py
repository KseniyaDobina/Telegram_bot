import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')
API_HOST = 'hotels4.p.rapidapi.com'
RAPID_URL = 'https://' + API_HOST
HEADERS = {
    'X-RapidAPI-Key': API_KEY,
    'X-RapidAPI-Host': API_HOST,
}
FIRST_ENDPOINTS = '/locations/v2/search'
SECOND_ENDPOINTS = '/properties/list'
THIRD_ENDPOINTS = '/properties/get-hotel-photos'
LIST_SORT = ('PRICE', 'PRICE_HIGHEST_FIRST', 'DISTANCE_FROM_LANDMARK')
DEFAULT_COMMANDS = [
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
    ('lowprice', 'Вывести самые дешёвые отели в городе'),
    ('highprice', 'Вывести самые дорогие отели в городе'),
    ('bestdeal', 'Вывести отели, наиболее подходящие по цене и расположению от центра'),
    ('history', 'Вывести историю поиска')
]
