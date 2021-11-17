import g
import api
import utils

def exec_tg_command(cmd: str, text: str, message: dict):
    t, s_peer = text.split()
    vk_peer = int(s_peer)
    match(t):
        case 'p':
            pass
        case 'g':
            vk_peer += 2000000000
        case 'c':
            vk_peer *= -1
        case _:
            g.logs.warning(
                f'Got unsupported chat type in command {cmd} of message {message}')
            raise Exception()
    match(cmd):
        case '/vkpeer':
            g.set_route(int(message['chat']['id']), vk_peer)


@g.ee.on('tg.msg')
@utils.tryexcept
def proc_tg_message(message: dict):
    if 'entities' in message:
        for entity in message['entities']:
            if entity['type'] == 'bot_command':
                if entity['offset'] != 0:
                    print('ignoring command')
                else:
                    cmd = message['text'][:entity['length']]
                    text = message['text'][entity['length']:].strip()
                    try:
                        exec_tg_command(cmd, text, message)
                    except Exception as e:
                        g.logs.warning(
                            f'Command {cmd} of message  failed! {message}\n Exception: {e}')
                        api.send_tg_message(message['chat']['id'],
                                            text='Your last command has failed')
    else:
        if g.tg_route(message['chat']['id']) is None:
            return
        try:
            vk_chat_peer = g.tg_route(message['chat']['id'])
            api.send_vk_message(vk_chat_peer, {'message': message['text']})
        except Exception as e:
            api.send_tg_message(message['chat']['id'], text='Cant process last message')
