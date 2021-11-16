import requests
import config
import utils
from threading import Thread, Lock
import g

mutex = Lock()


def _tg_method(method: str, data: dict = {}):
    res = requests.post(config.tokenized_tg_url + method, json=data)
    return res.json()


def _vk_method(method: str, data: dict = {}):
    params_str = 'access_token=' + config.vk_token + '&v=5.131&'
    params_str += '&'.join([key+'='+str(val) for key, val in data.items()])
    response = requests.get(config.base_vk_url + method + '/?' + params_str)
    return response.json()


def _tg_longpoll():
    updates_offset = 0
    while True:
        response = _tg_method('getUpdates', {
            'offset': updates_offset
        })
        if not response['ok']:
            g.logs.error("Failed to fetch telegram")
            continue

        updates = response['result']
        for update in updates:
            g.logs.debug("Got update: " + utils.dict_to_str(update))
            _single_tg_update(update)

            updates_offset = update['update_id'] + 1


def _init_vklongpoll():
    resp = _vk_method('messages.getLongPollServer')['response']
    return (resp['server'], resp['key'], resp['ts'])


def _vk_longpoll(server, key, ts):
    while True:
        req_str = f'https://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2&version=1'

        resp = requests.get(req_str).json()
        if 'failed' in resp:
            g.logs.error("Failed to fetch vk")
            continue

        ts = resp['ts']
        for update in resp['updates']:
            g.logs.debug("Got vk update: " + utils.dict_to_str(update))
            _single_vk_update(update)

def _init():
    vk_server_data = _init_vklongpoll()
    vk_thread = Thread(target=_vk_longpoll, args=vk_server_data)
    vk_thread.start()

    tg_thread = Thread(target=_tg_longpoll)
    tg_thread.start()

    g.logs.debug("network initialized")
_init()

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
            g.logs.debug('Sending message event')
            _throwEvent("tg.msg", update['message'])

        case _:
            g.logs.info("Incoming tg update didn't match any case")
