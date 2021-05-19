import asyncio
import pprint
from typing import Callable

import aiohttp
import requests

from . import get_uuid


# todo error handling
class PlayerNotFound(Exception):
    pass

from . import InvalidAPIKey, api_key


def get_auction(username: str, api_key: str) -> list[dict]:
    results = []
    is_bin = 'BIN'
    data = requests.get(f"https://api.hypixel.net/skyblock/auction?key={api_key}&player={get_uuid(username)}").json()
    try:
        for x in data['auctions']:
            if x['claimed']:
                pass
            else:
                try:
                    if x['bin']:
                        is_bin = 'BIN'
                    else:
                        is_bin = 'Auction'
                except KeyError:
                    is_bin = 'Auction'
                if is_bin == 'BIN':
                    results.append(
                        {'name': x['item_name'], 'cost': x['starting_bid'], 'rarity': x['tier'], 'type': is_bin})
                else:
                    bids = [f for f in x['bids']]
                    try:
                        results.append(
                            {'name': x['item_name'], 'highest bid': bids[len(bids) - 1]['amount'], 'rarity': x['tier'],
                             'type': is_bin})
                    except IndexError:
                        results.append(
                            {'name': x['item_name'], 'starting bid': x['highest_bid_amount'], 'rarity': x['tier'],
                             'type': is_bin})
    except KeyError:
        raise InvalidAPIKey

    return pprint.pformat(results)


class PlayerAuction:
    """Get active auction of a player"""

    def __init__(self, username: str, key: str=None):
        if key is None:
            from . import api_key as KEy
            self.key = KEy
        else:
            self.key = key
        self.username = username
        try:
            self.uuid = requests.get(f"https://api.ashcon.app/mojang/v2/user/{self.username}").json()["uuid"].replace(
                "-", "")
        except KeyError:
            raise PlayerNotFound(f'Could not find player with name: {self.username}')

    def get_auction(self):
        results = []
        is_bin = 'BIN'
        data = requests.get(f"https://api.hypixel.net/skyblock/auction?key={self.key}&player={self.uuid}").json()
        try:
            for x in data['auctions']:
                if x['claimed']:
                    pass
                else:
                    try:
                        if x['bin']:
                            is_bin = 'BIN'
                        else:
                            is_bin = 'Auction'
                    except KeyError:
                        is_bin = 'Auction'
                    if is_bin == 'BIN':
                        results.append(
                            {'name': x['item_name'], 'cost': x['starting_bid'], 'rarity': x['tier'], 'type': is_bin})
                    else:
                        bids = [f for f in x['bids']]
                        try:
                            results.append({'name': x['item_name'], 'highest bid': bids[len(bids) - 1]['amount'],
                                            'rarity': x['tier'], 'type': is_bin})
                        except IndexError:
                            results.append(
                                {'name': x['item_name'], 'starting bid': x['highest_bid_amount'], 'rarity': x['tier'],
                                 'type': is_bin})
        except KeyError:
            if not data['success']:
                raise InvalidAPIKey
        return pprint.pformat(results)


class AuctionHouse:

    def __init__(self, key: str=None):
        if key is None:
            from . import api_key as kEY
            self.api_key = kEY
        else:
            self.api_key = key

    def get(self) -> list[dict]:
        async def update_data(session, page, key):
            async with session.get(f'https://api.hypixel.net/skyblock/auctions?key={key}&page={page}') as r:
                page_info = await r.json()
                results = self.AuctionPage(page_info)
                return results.get_data()

        async def __start():
            async with aiohttp.ClientSession() as ses:
                start_loop = asyncio.get_event_loop()
                tasks = [asyncio.ensure_future(update_data(ses, page, self.api_key), loop=start_loop) for page in
                         range(0, 65)]
                return await asyncio.gather(*tasks)

        loop = asyncio.get_event_loop()
        execute = loop.create_task(__start())
        all_ah = loop.run_until_complete(execute)
        return pprint.pformat(all_ah)

    class AuctionPage:
        class __Auction:
            def __init__(self, auction):
                self.properies = 'None'
                if auction['claimed']:
                    pass
                else:
                    self.properies = {}
                    try:
                        if auction['bin']:
                            is_bin = 'BIN'
                        else:
                            is_bin = 'Auction'
                    except KeyError:
                        is_bin = 'Auction'
                    if is_bin == 'BIN':
                        self.properies['type'] = 'BIN'
                    else:
                        bids = [f for f in auction['bids']]
                        try:
                            # self.properies{'name' =  x['item_name'], 'highest bid': bids[len(bids) - 1]['amount'],
                            #                 'rarity': x['tier'], 'type': is_bin})
                            self.properies['highet bid'] = bids[len(bids) - 1]
                        except IndexError:
                            # {'name': x['item_name'], 'starting bid': x['highest_bid_amount'], 'rarity': x['tier'],
                            #  'type': is_bin})
                            self.properies['price'] = auction['highest_bid_amount']
                    self.properies = {'name': auction['item_name'], 'rarity': auction['tier']}
            
            def get_ah(self):
                return self.properies

        def __init__(self, data):
            self.auctions = []
            if data['success']:
                for auction in data['auctions']:
                    test_obj = self.__Auction(auction)
                    if test_obj.properies == 'None':
                        pass
                    else:
                        self.auctions.append(test_obj.get_ah())
        
        def get_data(self):
            return self.auctions
