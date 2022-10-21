def check_address(check_hotel):
    """
    Проверяет наличие у отеля адреса.
    :param check_hotel: проверяемый отель
    :return: Если адрес присутствет, то возвращается строка с адресом,
    если нет, то возвращается строка с коодинатами отеля.
    """
    try:
        address = check_hotel['address']['streetAddress']
        return f"\nАдрес: {address}"

    except KeyError:
        return f"\nЯ не смог найти адрес, но я могу вывести координаты отеля:" \
               f"\n\tШирина: {check_hotel['coordinate']['lat']}" \
               f"\n\tДолгота: {check_hotel['coordinate']['lon']}"


def check_price(check_hotel, days):
    """
    Проверяет наличие у отеля цены.
    :param check_hotel: проверяемый отель
    :param days: дни
    :return: Если цена присутствет, то возвращается строка с ценой в сутки и суммарная за все дни, а так же сама цена.
    Если цена отсутствует, то возвращаются строка о том, что цены нет,
    а так же 0.
    """
    try:
        price = check_hotel['ratePlan']['price']['current']
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
    :param check_hotel: проверяемый отель
    :return: Если расположение до центр присутствет, то возвращается строка с расположением до центра.
    Если цена отсутствует, то возвращаются строка о том, расположение до центра нет.
    """
    if check_hotel['landmarks'][0]['label'] == 'City center':
        return f"\nРасположение до центра: {check_hotel['landmarks'][0]['distance']}"
    return '\nУ отеля не указано расстояние до центра города (отель может находиться уже в центре города)'


def get_info_about_hotel(hotel, days):
    """
    Собираем и выводит полное описание отеля
    :param hotel: отель
    :param days: дни
    :return: описание отеля
    """
    price = check_price(hotel, days)
    text = f"Название отеля: {hotel['name']}" \
           f"{check_address(hotel)}" \
           f"{check_center(hotel)}" \
           f"{price[0]}" \
           f"\nСсылка на отель: hotels.com/ho{hotel['id']}"
    return hotel, price[1], text
