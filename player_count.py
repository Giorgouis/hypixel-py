import requests
import aiohttp
import asyncio
import pprint


from .auction import InvalidAPIKey

def get_online_players(key=None, detailed: bool=False):
    from . import api_key
    if api_key is None:
        if key is None:
            raise InvalidAPIKey('NoApiKey')
    elif key is None:
        key = api_key
    if detailed:
        data = requests.get(f'https://api.hypixel.net/counts?key={key}').json()
        return pprint.pformat({'lobby': int(data['games']['MAIN_LOBBY']['players']),
            'tournament_lobby': int(data['games']['TOURNAMENT_LOBBY']['players']),
            'smp': int(data['games']['SMP']['players']),
            'bedwars': int(data['games']['BEDWARS']['players']),
            'arcade': int(data['games']['ARCADE']['players']),
            'classic games': int(data['games']['LEGACY']['players']),
            'battleground': int(data['games']['BATTLEGROUND']['players']),
            'tntgames': int(data['games']['TNTGAMES']['players']),
            'skywars': int(data['games']['SKYWARS']['players']),
            'speedUHC': int(data['games']['SPEED_UHC']['players']),
            'walls': int(data['games']['WALLS3']['players']),
            'MCGO': int(data['games']['MCGO']['players']),
            'housing': int(data['games']['HOUSING']['players']),
            'UHC': int(data['games']['UHC']['players']),
            'survival games': int(data['games']['SURVIVAL_GAMES']['players']),
            'super smash': int(data['games']['SUPER_SMASH']['players']),
            'skyblock': int(data['games']['SKYBLOCK']['players']),
            'pit': int(data['games']['PIT']['players']),
            'duels': int(data['games']['DUELS']['players']),
            'build battle': int(data['games']['BUILD_BATTLE']['players']),
            'murder mystery': int(data['games']['MURDER_MYSTERY']['players']),
            'towerwars': int(data['games']['PROTOTYPE']['players']),
            'replay': int(data['games']['REPLAY']['players']),
            'limbo': int(data['games']['LIMBO']['players']),
            'idle': int(data['games']['IDLE']['players']),
            'queue': int(data['games']['QUEUE']['players'])
            })
    else:
        data = requests.get(f'https://api.hypixel.net/counts?key={key}')
        return int(data['playerCount'])
