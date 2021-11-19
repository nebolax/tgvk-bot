from . import *
import g


def proc_tg2vk_msg(msg: dict):
    if 'entities' in msg:
        if proc_entities(msg):
            return

    # if 'photo' in msg:




def proc_entities(msg: dict):
    was_command = False
    for entity in msg['entities']:
        if entity['type'] == 'bot_command':
            msg_with_botcmd(msg, entity['offset'], entity['length'])

    return was_command


def msg_with_botcmd(msg: dict, cmd_offset: int, cmd_length: int):
    cmd_text = msg['text'][cmd_offset:cmd_length][1:]
    cmd_args = msg['text'][cmd_offset+cmd_length:].strip()
    try:
        bot_command(cmd_text, cmd_args, msg)
    except Exception as e:
        g.logs.warning(f'Failed to process bot command {cmd_text} of message {msg}. Exception: {e}')
