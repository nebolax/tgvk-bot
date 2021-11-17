from . import network as net
import g
import config


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


def get_tg_photo_link(photo_variants: list):
    largest_height = 0
    largest_photoid = ''
    for variant in photo_variants:
        if variant['height'] > largest_height:
            largest_height = variant['height']
            largest_photoid = variant['file_id']

    g.logs.debug(largest_photoid)
    phid_resp = net._tg_method('getFile', {
        'file_id': largest_photoid
    })['result']

    return (
        config.base_tg_url + 'file/' +
        config.bot_token +
        phid_resp['file_path'])
