import json

with open('errors.json', 'r', encoding='utf-8') as f:
    test_list = json.load(f)
    test_list_hotels = test_list['data']['propertySearch']['properties']
    for hotel in test_list_hotels:
        print(hotel['destinationInfo'])
        print(hotel['destinationInfo']['distanceFromDestination']['value'])
        print()
