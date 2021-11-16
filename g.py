import json
import logging
import pymitter
import enum

logs = logging.getLogger("tgvk-bot")

logs.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('otp.md', 'wt')
stream_handler.setFormatter(logging.Formatter(
    f"%(levelname)s:%(filename)s.%(funcName)s - %(message)s"
))
file_handler.setFormatter(logging.Formatter(
    f"%(levelname)s:%(filename)s.%(funcName)s - %(message)s"
))
logs.addHandler(stream_handler)

ee = pymitter.EventEmitter()

my_vkid = 272986958

_state: dict
# first - tg_chat_id, second - vk_peer
_routes: list


class RouteType(enum.Enum):
    personal = 0
    group = 1
    community = 2


with open('state.json') as f:
    _state = json.loads(f.read())
    _routes = _state['routes']
    logs.debug(f'Loaded roads: {_routes}')


def set_route(tg_chat_id: int, vk_peer: int):
    for i in range(len(_routes)):
        if _routes[i][0] == tg_chat_id:
            del _routes[i]
    _routes.append((tg_chat_id, vk_peer))
    update_state(routes=_routes)
    logs.debug(
        f"Added road: vk_peer {vk_peer} is now connected to {tg_chat_id} telegram chat)")


def vk_route(vk_peer: int) -> int:
    for route in _routes:
        if route[1] == vk_peer:
            return route[0]
    logs.warning(f'Failed to find route for vk chat with peer {vk_peer}')
    return None


def tg_route(tg_chat_id: int) -> int:
    for route in _routes:
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


def update_state(**kwargs):
    for key, val in kwargs.items():
        _state[key] = val

    with open('state.json', 'w') as f:
        f.write(json.dumps(_state))

def state_val(name: str):
    return _state[name]
