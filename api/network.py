import requests
from threading import Thread, Lock

from store import User
import g
import events
import store

mutex = Lock()


def _tg_method(method: str, params: dict = {}):
    if method != 'getUpdates':
        g.logs.debug(f'TG-method: {method}, --- {params}')
    resp = requests.post(g.base_tg_url + g.bot_token +
                         method, json=params).json()
    if not resp['ok']:
        g.logs.error(
            f'Tg-method {method} failed. Params: {params}, Response: {resp}')
        return None
    return resp


def _vk_method(method: str, vk_token: str, params: dict = {}):
    vk_token = str(vk_token)
    params_str = 'access_token=' + vk_token + '&v=5.131&'
    params_str += '&'.join([key+'='+str(val) for key, val in params.items()])
    resp = requests.get(g.base_vk_url + method + '/?' + params_str).json()
    if 'error' in resp:
        if resp['error']['error_code'] == 6:
            return _vk_method(method, vk_token, params)
        g.logs.error(f'Vk-method failed!! Response: {resp}')
        return None
    return resp


def _tg_longpoll():
    updates_offset = g.state['tg_offset']
    while True:
        response = _tg_method('getUpdates', {
            'offset': updates_offset
        })

        updates = response['result']
        for update in updates:
            updates_offset = update['update_id'] + 1
            g.state['tg_offset'] = updates_offset
            _single_tg_update(update)


def _init_vklongpoll(user: User):
    resp = _vk_method('messages.getLongPollServer', user.vk_token)['response']
    return (resp['server'], resp['key'], resp['ts'])


def _vk_longpoll(user: User):
    server, key, ts = _init_vklongpoll(user)
    while True:
        req_str = f'https://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2&version=1'

        resp = requests.get(req_str).json()
        if 'failed' in resp:
            if resp['failed'] == 2:
                server, key, ts = _init_vklongpoll(user)
                g.logs.info('Renewed vk_longpoll key')
            else:
                g.logs.critical(f"Failed to fetch vk: {resp}")
            continue

        ts = resp['ts']
        for update in resp['updates']:
            _single_vk_update(update)


def start_new_vklongpoll(user: User):
    vk_thread = Thread(target=_vk_longpoll, args=(user,))
    vk_thread.start()


def _init_network():
    for user in store.all_users():
        start_new_vklongpoll(user)

    tg_thread = Thread(target=_tg_longpoll)
    tg_thread.start()

##################################################################
# Lower we are processing incoming updates and emit correscponding events


def _throwEvent(type: str, data):
    events.emit(type, data)


def _single_vk_update(update: list):
    match(update[0]):
        case 4:
            g.logs.debug(f'Got new message from vk: {update}')
            _throwEvent("vk.msg", update[1:])


def _single_tg_update(update: dict):
    match(list(update.keys())[1]):
        case 'message':
            g.logs.debug(f'Got new message from telegram: {update}')
            _throwEvent("tg.msg", update['message'])
