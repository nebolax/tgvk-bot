import store
from store import Route, ChatType
import g
import api


def bot_command(cmd: str, text_args: str, msg: dict):
    match(cmd):
        case 'vkpeer':
            proc_vkpeer_command(text_args, msg)


def proc_start_command(msg: dict):
    if msg['chat']['type'] != 'private':
        return
    g.state['waiting_token'] = g.state['waiting_token'] + [msg['chat']['id']]
    api.send_tg_message(msg['chat']['id'], {'text': g.welcome_message})


def proc_vkpeer_command(text_args: str, msg: dict):
    cmd_type, s_peer = text_args.split()
    vk_peer = int(s_peer)
    chat_type: ChatType

    match(cmd_type):
        case 'личный':
            chat_type = ChatType.Private
        case 'беседа':
            vk_peer += 2000000000
            chat_type = ChatType.Group

    store.new_route(Route(msg['chat']['id'], vk_peer, chat_type, msg['from']['id']))
