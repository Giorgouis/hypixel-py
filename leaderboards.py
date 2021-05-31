import requests
from pprint import pformat
import requests
from . import get_username
from . import InvalidAPIKey
def get_leaderboard(key=None):
    from . import api_key
    if key is None:
        if api_key is None:
            raise InvalidAPIKey('No API key specified')
        key = api_key
    data = requests.get(f'https://api.hypixel.net/leaderboards?key={key}').json()
    return pformat({
        'duels': {
            'weekly_wins': [get_username(x) for x in data['leaderboards']['DUELS'][0]['leaders']],
            'monthly_wins': [get_username(x) for x in data['leaderboards']['DUELS'][1]['leaders']],
        },
        'skywars': {
            'levels': [get_username(x) for x in data['leaderboards']['SKYWARS'][0]['leaders']],
            'wins': [get_username(x) for x in data['leaderboards']['SKYWARS'][2]['leaders']],
            'kills': [get_username(x) for x in data['leaderboards']['SKYWARS'][3]['leaders']]
        },
        'bedwars': {
            'levels': [get_username(x) for x in data['leaderboards']['BEDWARS'][0]['leaders']]
        }
    }, width=2, indent=4)
