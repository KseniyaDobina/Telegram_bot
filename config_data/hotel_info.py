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


def get_foto(list_foto, count):
    """

    """
    new_list_foto = [list_foto[cnt]['image']['url'] for cnt in range(count)]
    return new_list_foto


def get_info_about_hotel(hotel_list, hotel, days):
    """
    Собирает и выводит полное описание отеля
    :param hotel: отель
    :param days: дни
    :return: описание отеля
    """
    price = check_price(hotel_list, days)
    text = f"Название отеля: {hotel['name']}" \
           f"{check_center(hotel_list)}" \
           f"\nАдрес: {hotel['location']['address']['addressLine']}" \
           f"{price[0]}" \
           f"\nСсылка на отель: hotels.com/h{hotel['id']}.Hotel-Information"
    return price[1], text
