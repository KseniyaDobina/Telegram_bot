import requests
import json

from states import TownCard
from config_data import config


def request_to_api(url, headers, params):
    """
    Получает информацию с сайта.
    :param url: ссылка
    :param headers: headers
    :param params: params
    :return: json или информацию об ошибке
    """
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code == requests.codes.ok:
            return json.loads(response.text)

    except:
        return "Что-то пошло не так"


def sort_hotels(command):
    """
    Нахождит метод сортировки отелей
    :param command: команда
    :return: метод сортировки
    """
    if command == 'lowprice':
        return config.LIST_SORT[0]

    elif command == 'highprice':
        return config.LIST_SORT[1]

    else:
        return config.LIST_SORT[2]


def check_centre(list_hotels):
    """
    Проверяет наличие центра у отелей.
    :param list_hotels: список с отелями
    :return: список с отелями
    """
    find_id = float("inf")
    for id_c, count in enumerate(list_hotels):
        if count['landmarks'][0]['label'] != "City center":
            return []
        elif float(count['landmarks'][0]['distance'].split()[0]) > TownCard.max_landmark:
            find_id += 1
            break
        find_id = id_c

    if find_id < float("inf"):
        return list_hotels[:find_id]

    return list_hotels
