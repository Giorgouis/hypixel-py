import requests
from typing import Callable

api_key = None


class InvalidAPIKey(Exception):

    def __init__(self, message='Invalid API key'):
        self.message = message
        super().__init__(self.message)

get_uuid: Callable = lambda username: requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}').json()['id'].replace(
    "-", "")

get_username: Callable = lambda uuid: requests.get(f'https://api.mojang.com/user/profiles/{uuid}/names').json()[-1]['name']