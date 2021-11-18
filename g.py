import json
import logging
from typing import Callable
import pymitter
import enum

logs = logging.getLogger("tgvk-bot")

logs.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('otp.md', 'wt')
stream_handler.setFormatter(logging.Formatter(
    f"%(levelname)s:%(filename)s.%(funcName)s.%(lineno)d - %(message)s"
))
file_handler.setFormatter(logging.Formatter(
    f"%(levelname)s:%(filename)s.%(funcName)s.%(lineno)d - %(message)s"
))
logs.addHandler(stream_handler)
logs.addHandler(file_handler)

ee = pymitter.EventEmitter()

my_vkid = 272986958





state: ObservableDict
# first - tg_chat_id, second - vk_peer


class RouteType(enum.Enum):
    personal = 0
    group = 1
    community = 2


def _update_dict(full, nkey, nval):
    with open('state.json', 'w') as f:
        f.write(json.dumps(full))


with open('state.json') as f:
    state = ObservableDict(_update_dict, json.loads(f.read()))
    logs.debug(f"Loaded routes: {state['routes']}")


def set_route(tg_chat_id: int, vk_peer: int):
    for i in range(len(state['routes'])):
        if state['routes'][i][0] == tg_chat_id:
            del state['routes'][i]
    state['routes'].append((tg_chat_id, vk_peer))
    logs.debug(
        f"Added road: vk_peer {vk_peer} is now connected to {tg_chat_id} telegram chat)")


def vk_route(vk_peer: int) -> int:
    for route in state['routes']:
        if route[1] == vk_peer:
            return route[0]
    logs.warning(f'Failed to find route for vk chat with peer {vk_peer}')
    return None


def tg_route(tg_chat_id: int) -> int:
    for route in state['routes']:
        if route[0] == tg_chat_id:
            return route[1]
    logs.warning(f'Failed to find route for tg chat with id {tg_chat_id}')
    return None


def chat_type(vk_peer: int):
    if vk_peer > 2000000000:
        return RouteType.group
    if vk_peer < 0:
        return RouteType.community
    else:
        return RouteType.personal
