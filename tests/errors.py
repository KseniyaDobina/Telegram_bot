data = {
    'suggestions': [
        {
            'entities': []
        }
    ]
}

try:
    if len(data['suggestions']['1']['entities']) == 0:
        raise KeyError
except KeyError:
    print(125)
except TypeError:
    print(4)

# print(data['suggestions'][0]['entities'])
