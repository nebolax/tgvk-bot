import requests
import g, store
from threading import Thread, Lock

mutex = Lock()


def _tg_method(method: str, params: dict = {}):
    resp = requests.post(g.base_tg_url + g.bot_token + method, json=params).json()
    if not resp['ok']:
        g.logs.error(f'Tg-method {method} failed. Params: {params}, Response: {resp}')
        return None
    return resp


def _vk_method(method: str, user_tgid: int, params: dict = {}):
    vktoken = store.user_by_tgid(user_tgid)['vktoken']
    params_str = 'access_token=' + vktoken + '&v=5.131&'
    params_str += '&'.join([key+'='+str(val) for key, val in params.items()])
    resp = requests.get(g.base_vk_url + method + '/?' + params_str).json()
    if 'error' in resp:
        g.logs.error(f'Vk-method failed!! Response: {resp}')
        return None
    return resp


def _tg_longpoll():
    updates_offset = g.state['tg_offset']
    while True:
        response = _tg_method('getUpdates', {
            'offset': updates_offset
        })
        if not response['ok']:
            g.logs.critical(f"Failed to fetch telegram: {response}")
            continue

        updates = response['result']
        for update in updates:
            updates_offset = update['update_id'] + 1
            g.state['tg_offset'] = updates_offset
            _single_tg_update(update)


def _init_vklongpoll(user_tgid: int):
    resp = _vk_method('messages.getLongPollServer', user_tgid)['response']
    return (resp['server'], resp['key'], resp['ts'])


def _vk_longpoll(user_tgid: int):
    server, key, ts = _init_vklongpoll(user_tgid)
    while True:
        req_str = f'https://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2&version=1'

        resp = requests.get(req_str).json()
        if 'failed' in resp:
            if resp['failed'] == 2:
                server, key, ts = _init_vklongpoll(user_tgid)
                g.logs.info('Renewed vk_longpoll key')
            else:
                g.logs.critical(f"Failed to fetch vk: {resp}")
            continue

        ts = resp['ts']
        for update in resp['updates']:
            _single_vk_update(update)

def start_new_vklongpoll(tg_userid: int):
    vk_thread = Thread(target=_vk_longpoll, args=(tg_userid,))
    vk_thread.start()

def _init():
    for user_tgid in store.all_users_tgids():
        start_new_vklongpoll(user_tgid)

    tg_thread = Thread(target=_tg_longpoll)
    tg_thread.start()

##################################################################
# Lower we are processing incoming updates and emit correscponding events

def _throwEvent(type: str, data):
    with mutex:
        g.ee.emit(type, data)


def _single_vk_update(update: list):
    match(update[0]):
        case 4:
            _throwEvent("vk.msg", update[1:])



def _single_tg_update(update: dict):
    if len(update.keys()) > 2:
        g.logs.critical("Tg can have more than 2 keys!: " + str(update.keys()))

    match(list(update.keys())[1]):
        case 'message':
            _throwEvent("tg.msg", update['message'])

##########################################################3
_init()