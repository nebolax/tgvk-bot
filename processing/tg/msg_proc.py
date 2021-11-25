from store import routes, User
import store, api
from .commands_proc import *
import g


def proc_tg2vk_msg(msg: dict):
    if 'entities' in msg:
        if proc_entities(msg):
            return
            
    if store.route_by_tgchatid(msg['chat']['id']) is None:
        api.send_tg_message(msg['chat']['id'], {
            'text': 'Установите беседу, к которой нужно подключиться. Для инструкции отправьте /help боту в личные сообщения'
        })
        return

    api.send_vk_message(routes.route_by_tgchatid(msg['chat']['id']), {
        'message': msg['text']
    })


def proc_entities(msg: dict):
    was_command = False
    for entity in msg['entities']:
        if entity['type'] == 'bot_command':
            was_command = True
            msg_with_botcmd(msg, entity['offset'], entity['length'])

    return was_command


def msg_with_botcmd(msg: dict, cmd_offset: int, cmd_length: int):
    cmd_text = msg['text'][cmd_offset:cmd_length][1:]
    cmd_args = msg['text'][cmd_offset+cmd_length:].strip()
    try:
        bot_command(cmd_text, cmd_args, msg)
    except Exception as e:
        g.logs.warning(
            f'Failed to process bot command {cmd_text} of message {msg}. Exception: {e}')

def token_passed(msg: dict, vk_userid: int, vk_token: str):
    new_user = User(msg['from']['id'], vk_userid, vk_token)
    store.new_user(new_user)
    api.start_new_vklongpoll(new_user)
    api.send_tg_message(msg['chat']['id'], {
        'text': 'Поздравляю с успешной авторизацией!'})
    g.state['waiting_token'] = list(
        filter(lambda chatid: chatid != msg['chat']['id'], g.state['waiting_token']))
