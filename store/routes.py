from g import RouteType, SavingDict

# route = 'tg_chatid': {'vk_peer': val, 'tg_userid': val, 'vk_userid': val}


def routes_by_vkpeer(vk_peer: int) -> list[dict]:
    res = []
    for tg_chatid, val in _routes.values():
        if val['vk_peer'] == vk_peer:
            res.append(dict(**val, tg_chatid=tg_chatid))
    return res


def route_by_tgchatid(tg_chatid: int):
    if tg_chatid not in _routes:
        return None
    return dict(**_routes[tg_chatid], tg_chatid=tg_chatid)


def routes_by_tguserid(tg_userid: int):
    res = []
    for tg_chatid, val in _routes.values():
        if val['tg_userid'] == tg_userid:
            res.append(dict(**val, tg_chatid=tg_chatid))
    return res


def routes_by_vkuserid(vk_userid: int):
    res = []
    for tg_chatid, val in _routes.values():
        if val['vk_userid'] == vk_userid:
            res.append(dict(**val, tg_chatid=tg_chatid))
    return res

def _chat_type(vk_peer: int):
    if vk_peer > 2000000000:
        return RouteType.group
    if vk_peer < 0:
        return RouteType.community
    else:
        return RouteType.personal


def new_route(tg_chatid, vk_peer, tg_userid, vk_userid):
    _routes[tg_chatid] = {
        'vk_peer': vk_peer,
        'chat_type': _chat_type(vk_peer),
        'tg_userid': tg_userid,
        'vk_userid': vk_userid
    }


_routes = utils.SavingDict('routes.json')
