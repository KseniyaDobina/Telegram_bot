import json


def find_center():
    find_id = float("inf")
    with open('json_parse.json') as file:
        data = json.load(file)

    for id_c, count in enumerate(data):
        if count['landmarks'][0]['label'] != "City center":
            print('Нет центра')
        elif float(count['landmarks'][0]['distance'].split()[0]) > 0.1:
            print(find_id)
            break
        print(float(count['landmarks'][0]['distance'].split()[0]), 0.1)
        find_id = id_c

    new_data = {}

    if find_id < float("inf"):
        new_data = data[:find_id + 1]
    for i in data:
        print(i['landmarks'][0]['distance'])
    print()
    for i in new_data:
        print(i['landmarks'][0]['distance'])


def print_info():
    with open('json_parse.json') as file:
        data = json.load(file)

    for i in data:
        print(i['id'], i['name'])


print_info()
