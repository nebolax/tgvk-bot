import g


def user_by_tgid(tgid: int) -> dict:
    if tgid not in _users:
        return None
    return dict(**_users[tgid], tgid=tgid)


def user_by_vkid(vkid: int) -> dict:
    for tgid, val in _users.items():
        if val['vkid'] == vkid:
            return dict(**val, tgid=tgid)
    return None


def new_user(tgid: int, vkid: int, vktoken: str) -> None:
    if tgid in _users:
        g.logs.warning(f'Re-registering user with tg id {tgid}')

    _users[tgid] = {
        'vkid': vkid,
        'vktoken': vktoken,
    }


def all_users_tgids() -> list[dict]:
    return _users.keys()


_users = g.SavingDict('users.json')
