from . import *
import g
import api
import store
import re


def tg_route(msg: dict):
    if msg['chat']['id'] in g.state['waiting_token']:
        token_msg(msg)
    elif msg['text'] == 'start':
        proc_start_command(msg)
    elif store.user_by_tgid(msg['from']['id']) is None:
        api.send_tg_message(msg['chat']['id'], {
                            'text': 'Перед использованием бота выполните его настройку @tgvk_connectbot'})
    else:
        proc_tg2vk_msg(msg)


def token_msg(msg: dict):
    token_search = re.search(r'access_token=(.+?)&', msg['text'])
    userid_search = re.search(r'user_id=(.+)')
    if token_search is None or userid_search is None:
        api.send_tg_msg(msg['chat']['id'], {
            'text': 'Некорректная ссылка. Попробуйте еще раз'})
    else:
        store.new_user(msg['from']['id'], userid_search.group(
            1), token_search.group(1))
        api.start_new_vklongpoll(msg['from']['id'])
        api.send_tg_msg(msg['chat']['id'], {
                        'text': 'Поздравляю с успешной авторизацией!'})
