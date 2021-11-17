import requests
from api.vk_api import person_name
import config
from threading import Thread, Lock
import g
from utils import dict_to_str

mutex = Lock()


def _tg_method(method: str, params: dict = {}):
    resp = requests.post(config.tokenized_tg_url + method, json=params).json()
    if not resp['ok']:
        g.logs.error('Tg-method failed')
    return resp


def _vk_method(method: str, params: dict = {}):
    params_str = 'access_token=' + config.vk_token + '&v=5.131&'
    params_str += '&'.join([key+'='+str(val) for key, val in params.items()])
    resp = requests.get(config.base_vk_url + method + '/?' + params_str).json()
    if 'error' in resp:
        g.logs.error(f'Vk-method failed!! Response: {resp}')
    return resp


def _tg_longpoll():
    updates_offset = g.state_val('tg_offset')
    while True:
        response = _tg_method('getUpdates', {
            'offset': updates_offset
        })
        if not response['ok']:
            g.logs.critical(f"Failed to fetch telegram: {response}")
            input()
            continue

        updates = response['result']
        for update in updates:
            updates_offset = update['update_id'] + 1
            g.update_state(tg_offset = updates_offset)
            _single_tg_update(update)


def _init_vklongpoll():
    resp = _vk_method('messages.getLongPollServer')['response']
    return (resp['server'], resp['key'], resp['ts'])


def _vk_longpoll(server, key, ts):
    while True:
        req_str = f'https://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2&version=1'

        resp = requests.get(req_str).json()
        if 'failed' in resp:
            if resp['failed'] == 2:
                server, key, ts = _init_vklongpoll()
                g.logs.info('Renewed vk_longpoll key')
            g.logs.critical(f"Failed to fetch vk: {resp}")
            input()
            continue

        ts = resp['ts']
        for update in resp['updates']:
            _single_vk_update(update)

def _init():
    vk_server_data = _init_vklongpoll()
    vk_thread = Thread(target=_vk_longpoll, args=vk_server_data)
    vk_thread.start()

    tg_thread = Thread(target=_tg_longpoll)
    tg_thread.start()

    # resp = _vk_method('messages.getHistoryAttachments', {
    #     'peer_id': 2000000173,
    #     'media_type': 'photo'
    # })
    # g.logs.debug(resp)

    g.logs.debug("network initialized")

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