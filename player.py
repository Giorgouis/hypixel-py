import requests
import math


def get_status(username: str, key: str=None) -> dict:
    if key is None:
        from . import api_key, InvalidAPIKey
        if api_key is None:
            raise InvalidAPIKey('No API Key Found')
        key = api_key
    from . import get_uuid
    data = requests.get(f'https://api.hypixel.net/status?uuid={get_uuid(username)}&key={key}').json()
    return data['session']


def get_stats(username: str, key: str=None) -> dict:
    # https://api.hypixel.net/player
    if key is None:
        from . import api_key, InvalidAPIKey
        if api_key is None:
            raise InvalidAPIKey('No API Key Found')
        key = api_key
    from . import get_uuid
    data = requests.get(f'https://api.hypixel.net/player?uuid={get_uuid(username)}&key={key}').json()
    return {'achievement points': int(data['player']['achievementPoints']), 
        'karma': int(data['player']['karma']),
        'level': (math.sqrt((2 * float(data['player']['networkExp'])) + 30625) / 50) - 2.5
    }


'''
# Get Level
network_experience = hypixel_data["player"]["networkExp"]
network_level = (math.sqrt((2 * network_experience) + 30625) / 50) - 2.5
network_level = round(network_level, 2)

'''