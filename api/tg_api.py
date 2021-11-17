from . import network as net
import g

def send_tg_message(chat_id: int, params: dict):
    params['chat_id'] = chat_id
    params['parse_mode'] = 'HTML'
    net._tg_method('sendMessage', params)

def send_tg_photos(chat_id: int, params: dict, caption: str = ''):
    params['chat_id'] = chat_id
    # params['text'] = 'azuzizazu'
    params['media'][0]['parse_mode'] = 'HTML'
    params['media'][0]['caption'] = caption
    net._tg_method('sendMediaGroup', params)