import random
import requests
from api.vk_api import vk_person_name
import g
import store
from threading import Thread, Lock
import time
from tqdm import tqdm

mutex = Lock()


@g.tryexcept
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


@g.tryexcept
def _vk_method(method: str, user_tgid: int, params: dict = {}):
    g.logs.debug(f'VK-method: {method}, --- {user_tgid}, --- {params}')
    vktoken = store.user_by_tgid(user_tgid)['vktoken'][random.randint(0, 1)]
    params_str = 'access_token=' + vktoken + '&v=5.131&'
    params_str += '&'.join([key+'='+str(val) for key, val in params.items()])
    resp = requests.get(g.base_vk_url + method + '/?' + params_str).json()
    if 'error' in resp:
        if resp['error']['error_code'] == 6:
            return _vk_method(method, user_tgid, params)
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


@g.tryexcept
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


@g.tryexcept
def start_new_vklongpoll(tg_userid: int):
    vk_thread = Thread(target=_vk_longpoll, args=(tg_userid,))
    vk_thread.start()


def init():
    mid_time = 0
    start = time.time()
    for i in tqdm(range(37)):
        r1 = _vk_method('messages.getConversations', 327150749,  {
            'count': 10,
            'offset': 5
        })['response']['items']
        r2 = []
        for el in list(r1):
            # print(g.dict_to_str(el))
            peer_id = int(el['conversation']['peer']['id'])
            # try:
            chname = ''
            if el['conversation']['peer']['type'] == 'chat':
                chname = el['conversation']['chat_settings']['title']
            else:
                chname = vk_person_name(peer_id, 327150749)
            # if chid >= 2000000000:
            #     chid -= 2000000000
            # elif chid < 0:
            #     chid *= -1

            r2.append({str(peer_id): chname})
            # print(rp['response']['title'])
            # except Exception as e:
            #     r2.append(f'{chid} has error: {e}')
            # print(f'{chid} is skipped')
            # time.sleep(0.1)
    mid_time = (time.time() - start) / 37
    g.logs.critical(f'Taken time: {mid_time}')
    # g.logs.critical(g.dict_to_str(r2))
    for user_tgid in store.all_users_tgids():
        start_new_vklongpoll(user_tgid)

    tg_thread = Thread(target=_tg_longpoll)
    tg_thread.start()

##################################################################
# Lower we are processing incoming updates and emit correscponding events


def _throwEvent(type: str, data):
    with mutex:
        g.ee.emit(type, data)


@g.tryexcept
def _single_vk_update(update: list):
    match(update[0]):
        case 4:
            g.logs.debug(f'Got new message from vk: {update}')
            _throwEvent("vk.msg", update[1:])


@g.tryexcept
def _single_tg_update(update: dict):
    if len(update.keys()) > 2:
        g.logs.critical("Tg can have more than 2 keys!: " + str(update.keys()))

    match(list(update.keys())[1]):
        case 'message':
            g.logs.debug(f'Got new message from telegram: {update}')
            _throwEvent("tg.msg", update['message'])


init()
