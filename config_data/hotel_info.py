from config_data.config import RAPID_URL, THIRD_ENDPOINTS, HEADERS

from config_data.parse import request_to_api


def check_price(check_hotel, days):
    """
    Проверяет наличие у отеля цены.
    :param check_hotel: Проверяемый отель
    :param days: дни
    :return: Если цена присутствует, то возвращается строка с ценой в сутки и суммарная за все дни, а так же сама цена.
    Если цена отсутствует, то возвращаются строка о том, что цены нет,
    а так же 0.
    """
    try:
        price = check_hotel['price']['options'][0]['formattedDisplayPrice']
        if ',' in price:
            price = int(''.join(price[1:].split(',')))

        else:
            price = int(price[1:])

        return f"\nЦена за сутки: ${price}" \
               f"\nСуммарная стоимость за все дни: ${days.days * price}", price

    except KeyError:
        return f"\nЯ не смог найти цену за сутки. Для расчета стоимости перейдите по ссылке ниже.", 0


def check_center(check_hotel):
    """
    Проверяет наличие у отеля расположения до центра.
    :param check_hotel: Проверяемый отель
    :return: Если расположение до центра присутствует, то возвращается строка с расположением до центра.
    Если цена отсутствует, то возвращаются строка о том, расположение до центра нет.
    """
    try:
        return (f"\nРасположение до центра: {check_hotel['destinationInfo']['distanceFromDestination']['value']} "
                f"километров.")
    except KeyError:
        return '\nУ отеля не указано расстояние до центра города (отель может находиться уже в центре города)'


def get_info_about_hotel(hotel, days, foto=False):
    """
    Собираем и выводит полное описание отеля
    :param hotel: отель
    :param days: дни
    :return: описание отеля
    """
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": str(hotel['id'])
    }
    answer = request_to_api(url=RAPID_URL + THIRD_ENDPOINTS, headers=HEADERS, params=payload, post=True)

    hotel_detail = answer['data']['propertyInfo']['summary']
    price = check_price(hotel, days)
    text = f"Название отеля: {hotel['name']}" \
           f"{check_center(hotel)}" \
           f"\nАдрес: {hotel_detail['location']['address']['addressLine']}" \
           f"{price[0]}" \
           f"\nСсылка на отель: hotels.com/h{hotel['id']}.Hotel-Information"
    return hotel, price[1], text
