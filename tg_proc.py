import g
from network import send_tg_message

def exec_tg_command(cmd: str, text: str, message: dict):
    t, s_peer = text.split()
    vk_peer = int(s_peer)
    if t == 'g':
        vk_peer += 2000000000
    match(cmd):
        case '/vkpeer':
            g.add_road(vk_peer, int(message['chat']['id']))

@g.ee.on('tg.msg')
def proc_tg_message(message: dict):
    g.logs.debug("Catched message event")
    if 'entities' in message:
        for entity in message['entities']:
            if entity['type'] == 'bot_command':
                if entity['offset'] != 0:
                    print('ignoring command')
                else:
                    cmd = message['text'][:entity['length']]
                    text = message['text'][entity['length']:].strip()
                    exec_tg_command(cmd, text, message)
    else:
        if message['chat']['id'] not in g.tg_roads:
            print('This chat peer is not specified')
            return
        vk_chat_peer = g.tg_roads[message['chat']['id']]
        message_to_vk(vk_chat_peer, message['text'])
        send_tg_message(message['chat']['id'], message['text'])