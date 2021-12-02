from dataclasses import dataclass
import re

import api
import events
import g
import store as db

from . import *
from .commands_proc import *
from .msg_proc import *


@events.on('tg.msg')
def tg_route(inp_msg: dict):
    msg = TgMsg(inp_msg)
    if msg.chat_id in g.state['waiting_token']:
        token_msg()
    elif msg.text == '/start':
        proc_start_command(msg)
    elif msg.sender is None:
        api.send_tg_message(msg.chat_id, {
                            'text': 'Перед использованием бота выполните его настройку @tg2vk_connectbot'})
    else:
        proc_tg2vk_msg(msg)


@events.on('tg.button')
def tg_chat_choosed(inp_msg: dict):
    user_id = int(inp_msg['from']['id'])
    source_msg = TgMsg(inp_msg['message'])
    callback_data = inp_msg['data']

    vk_peer = int(callback_data)
    print(vk_peer)
    convs_vars = g.state[f'peer_setup_{source_msg.chat_id}']
    cur_conv_info = list(filter(lambda x: vk_peer == x['peer'], convs_vars))[0]
    conv = VkConversation(cur_conv_info['peer'], cur_conv_info['title'], ChatType(cur_conv_info['chat_type']))

    db.sql.delete(db.sql.query(Route).filter(Route.tg_chat_id == source_msg.chat_id).first())
    db.sql.add(Route(source_msg.chat_id, vk_peer,
               conv.chat_type, user_id))
    db.sql.commit()

    api.tg_delete_msg(source_msg.chat_id, source_msg.id)

    api.send_tg_message(source_msg.chat_id, {
        'text': f'Отлично! Теперь этот чат связан с чатом {conv.title} из ВК!'
    })
