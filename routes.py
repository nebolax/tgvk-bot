import utils
import json

# route = ['tg_chatid', 'vk_peer', 'tg_userid', 'vk_userid']

def _update_routes():
    with open('routes.json', 'w') as f:
        f.write(json.dumps(_routes))

with open('routes.json') as f:
    _routes = utils.ObservableDict(_update_routes, json.loads(f.read()))

def new_route(tg_chatid, vk_peer, tg_userid, vk_userid):
    _routes.append(tg_chatid, vk_peer, tg_userid, vk_userid)