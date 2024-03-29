import requests
import json

from states import TownCard
from config_data import config


def request_to_api(url, headers, params, post=False):
    """
    Получает информацию с сайта.
    :param url: Ссылка
    :param headers: headers
    :param params: params
    :param post: POST или GET запрос
    :return: json или информацию об ошибке
    """
    try:
        if post:
            headers_for_post = headers
            headers_for_post['content-type'] = 'application/json'
            response = requests.post(url, json=params, headers=headers_for_post, timeout=40)
        else:
            response = requests.get(url, headers=headers, params=params, timeout=40)

        if response.status_code == requests.codes.ok:
            return json.loads(response.text)
        else:
            raise Exception

    except Exception:
        print(response.status_code, url)
        print("Что-то пошло не так")
        # return "Что-то пошло не так"


def sort_hotels(command):
    """
    Находит метод сортировки отелей
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
    :param list_hotels: Список с отелями
    :return: список с отелями
    """
    find_id = float("inf")
    for id_hotel, hotel in enumerate(list_hotels):
        try:
            if hotel['destinationInfo']['distanceFromDestination']['value'] > TownCard.max_landmark:
                find_id += 1
                break
        except KeyError:
            return []
        find_id = id_hotel

    if find_id < float("inf"):
        return list_hotels[:find_id]

    return list_hotels
