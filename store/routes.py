from g import SavingDict
import g

# route = 'tg_chatid': {'vk_peer': val, 'tg_userid': val, 'vk_userid': val}


def routes_by_vkpeer(vk_peer: int) -> list[dict]:
    vk_peer = str(vk_peer)
    res = []
    for tg_chatid, val in _routes.items():
        if val['vk_peer'] == vk_peer:
            res.append(dict(**val, tg_chatid=tg_chatid))
    return res


def route_by_tgchatid(tg_chatid: int):
    tg_chatid = str(tg_chatid)
    if tg_chatid not in _routes:
        return None
    return dict(**_routes[tg_chatid], tg_chatid=tg_chatid)


def routes_by_tguserid(tg_userid: int):
    tg_userid = str(tg_userid)
    res = []
    for tg_chatid, val in _routes.values():
        if val['tg_userid'] == tg_userid:
            res.append(dict(**val, tg_chatid=tg_chatid))
    return res


def routes_by_vkuserid(vk_userid: int):
    vk_userid = str(vk_userid)
    res = []
    for tg_chatid, val in _routes.values():
        if val['vk_userid'] == vk_userid:
            res.append(dict(**val, tg_chatid=tg_chatid))
    return res

def _chat_type(vk_peer: int):
    vk_peer = int(vk_peer)
    if vk_peer > 2000000000:
        return 'group'
    else:
        return 'personal'


def new_route(tg_chatid, vk_peer, tg_userid, vk_userid):
    _routes[str(tg_chatid)] = {
        'vk_peer': str(vk_peer),
        'chat_type': _chat_type(vk_peer),
        'tg_userid': str(tg_userid),
        'vk_userid': str(vk_userid)
    }


_routes = SavingDict('routes.json')
