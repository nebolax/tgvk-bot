import re

import api
import events
import g

from .msg_proc import *


@events.on('tg.msg')
def tg_route(msg: dict):
    if msg['chat']['id'] in g.state['waiting_token']:
        token_msg(msg)
    elif msg['text'] == '/start':
        proc_start_command(msg)
    elif store.user_by_tgid(msg['from']['id']) is None:
        api.send_tg_message(msg['chat']['id'], {
                            'text': 'Перед использованием бота выполните его настройку @tg2vk_connectbot'})
    else:
        proc_tg2vk_msg(msg)


def token_msg(msg: dict):
    token_search = re.search(r'access_token=(.+?)&', msg['text'])
    userid_search = re.search(r'user_id=(.+)', msg['text'])
    if token_search is None or userid_search is None:
        api.send_tg_message(msg['chat']['id'], {
            'text': 'Некорректная ссылка. Попробуйте еще раз'})
    else:
        token_passed(msg, userid_search.group(1), token_search.group(1))
