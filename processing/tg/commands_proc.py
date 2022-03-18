from processing.tg.tools import TgChatType, TgMsg
import store
from store import Route, ChatType
import g
import api


def bot_command(cmd: str, text_args: str, msg: TgMsg):
    match(cmd):
        case 'set_chat':
            proc_vkpeer_command(text_args, msg)
        case 'help':
            send_help(msg)


def send_help(msg: TgMsg):
    api.send_tg_message(msg.chat_id, {
        'text': g.help_message
    })


def proc_start_command(msg: TgMsg):
    if msg.chat_type != TgChatType.private:
        return
    g.state['waiting_token'] = g.state['waiting_token'] + \
        [msg.chat_id]
    api.send_tg_message(msg.chat_id, {'text': g.welcome_message})


def proc_vkpeer_command(text_args: str, msg: TgMsg):
    # cmd_type, s_peer = text_args.split()
    # vk_peer = int(s_peer)
    # chat_type: ChatType

    # match(cmd_type):
    #     case 'личный':
    #         chat_type = ChatType.Private
    #     case 'беседа':
    #         vk_peer += 2000000000
    #         chat_type = ChatType.Group

    # r = Route(msg.source_chat_id, vk_peer, chat_type, msg.sender_id)
    # store.new_route(r)
    print('**********')
    convs = api.get_conversations(msg.sender, 10, 0)
    keyboard = []
    for conv in convs:
        keyboard.append({
            'text': conv.title,
            'callback_data': str(conv.peer)
        })
    api.send_tg_message(msg.chat_id, {
        'text': 'Выберите чат для подключения',
        'reply_markup': {
            'inline_keyboard': list(zip(keyboard[:5], keyboard[5:]))
        }
    })['message_id']

    # print('**********' + str(chooser_msg_id) + '****************')
    g.state[f'peer_setup_{msg.chat_id}'] = list(map(lambda x: {
        'title': x.title,
        'peer': x.peer,
        'chat_type': x.chat_type.value
    }, convs))
