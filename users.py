import json
import utils, g


def _update_users():
    with open('users.json', 'w') as f:
        f.write(json.dumps(_users))

def user_bytgid(tgid):
    for user in _users:
        if user['tgid'] == tgid:
            return user
    return None

def user_byvkid(vkid):
    for user in _users:
        if user['vkid'] == vkid:
            return user
    return None

def new_user(tgid, vkid, vktoken):
    tgid = int(tgid)
    vkid = int(vkid)
    if tgid in _users:
        g.logs.warning(f'Re-registering user with tg id {tgid}')
    
    _users[tgid] = {
        'tg_id': tgid,
        'vk_id': vkid,
        'vktoken': vktoken,
    }
    
with open('users.json') as f:
    _users = utils.ObservableDict(_update_users, json.loads(f.read()))