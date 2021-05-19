import requests

from . import api_key
from . import InvalidAPIKey
from . import get_username
def get_key_info(key: str=None):
    if key is None:
        from . import api_key
        if api_key is None:
            raise InvalidAPIKey('No API Key specified')
        key = api_key
    data = requests.get(f'https://api.hypixel.net/key?key={key}').json()
    return {
        'owner': get_username(data['record']['owner']),
        'limit': int(data['record']['limit']),
        'queries': {
            'total': int(data['record']['totalQueries']),
            'past min': int(data['record']['queriesInPastMin'])
        }
    }