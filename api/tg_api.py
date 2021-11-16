from . import network as net
import g

def send_tg_message(chat_id: int, **params: dict):
    params['chat_id'] = chat_id
    params['parse_mode'] = 'HTML'
    net._tg_method('sendMessage', params)