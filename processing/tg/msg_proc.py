import re
from processing.tg.tools import TgMsg
from store import *
import store
import api
from .commands_proc import *
import g


def proc_tg2vk_msg(msg: TgMsg):
    if msg.entities != []:
        if proc_entities(msg):
            return

    # if msg.route is None:
    #     api.send_tg_message(msg.route.tg_chat_id, {
    #         'text': 'Установите беседу, к которой нужно подключиться. Для инструкции отправьте /help боту в личные сообщения'
    #     })
    #     return

    api.send_vk_message(sql.query(Route).filter(Route.tg_chat_id == msg.chat_id).first(), {
        'message': msg.text
    })


def proc_entities(msg: TgMsg):
    was_command = False
    for entity in msg.entities:
        if entity.type == 'bot_command':
            was_command = True
            msg_with_botcmd(msg, entity.offset, entity.length)

    return was_command


def msg_with_botcmd(msg: TgMsg, cmd_offset: int, cmd_length: int):
    cmd_text = msg.text[cmd_offset:cmd_length][1:]
    cmd_args = msg.text[cmd_offset+cmd_length:].strip()
    try:
        bot_command(cmd_text, cmd_args, msg)
    except Exception as e:
        g.logs.warning(
            f'Failed to process bot command {cmd_text} of message {msg}. Exception: {e}')


def token_passed(msg: TgMsg, vk_userid: int, vk_token: str):
    new_user = User(msg.sender_id, vk_userid, vk_token)
    store.sql().add(new_user)
    api.start_new_vklongpoll(new_user)
    api.send_tg_message(msg.chat_id, {
        'text': 'Поздравляю с успешной авторизацией!'})
    g.state['waiting_token'] = list(
        filter(lambda chatid: chatid != msg.chat_id, g.state['waiting_token']))


def token_msg(msg: TgMsg):
    token_search = re.search(r'access_token=(.+?)&', msg.text)
    userid_search = re.search(r'user_id=(.+)', msg.text)
    if token_search is None or userid_search is None:
        api.send_tg_message(msg.chat_id, {
            'text': 'Некорректная ссылка. Попробуйте еще раз'})
    else:
        token_passed(msg, userid_search.group(1), token_search.group(1))
