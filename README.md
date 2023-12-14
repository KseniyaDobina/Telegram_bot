# Телеграм бот


## Описание
Проект состоит из скрипта main.py и Telegram-бота с ником.
Пользователь с помощью специальных команд бота может выполнить следующие
действия (получить следующую информацию):
1. Узнать топ самых дешёвых отелей в городе (команда /lowprice).
2. Узнать топ самых дорогих отелей в городе (команда /highprice).
3. Узнать топ отелей, наиболее подходящих по цене и расположению от центра
(самые дешёвые и находятся ближе всего к центру) (команда /bestdeal).
4. Узнать историю поиска отелей (команда /history)


## Запуск
- Создать виртуальное окружение: `python -m venv venv`
- Установить нужные библиотеки: `pip install -r requirements.txt`
- Создать *.env* файл и внести в него токен своего бота и api. Пример: *env.template*
- Запустить бота: `python main.py`

## Описание работы команд

**Команда /lowprice**  
После ввода команды у пользователя запрашивается: 
1. Город, где будет проводиться поиск.
2. Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
3. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
   1. При положительном ответе пользователь также вводит количество
   необходимых фотографий (не больше заранее определённого
   максимума)

**Команда /highprice**  
После ввода команды у пользователя запрашивается:
1. Город, где будет проводиться поиск.
2. Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
3. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
   1. При положительном ответе пользователь также вводит количество
   необходимых фотографий (не больше заранее определённого
   максимума)


**Команда /bestdeal**  
После ввода команды у пользователя запрашивается:
1. Город, где будет проводиться поиск.
2. Диапазон цен.
3. Диапазон расстояния, на котором находится отель от центра.
4. Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
5. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
   1. При положительном ответе пользователь также вводит количество
   необходимых фотографий (не больше заранее определённого
   максимума)

**Команда /history**  
После ввода команды пользователю выводится история поиска отелей. Сама история
содержит:
1. Команду, которую вводил пользователь.
2. Дату и время ввода команды.
3. Отели, которые были найдены.
