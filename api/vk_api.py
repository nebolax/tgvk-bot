from store.routes import routes_by_vkpeer
from store.users import user_by_vkid
from . import network as net
import random

def send_vk_message(peer_id: int, params: dict):
    user_tgid = routes_by_vkpeer(peer_id)['tg_userid']
    params['peer_id'] = peer_id
    params['random_id'] = random.getrandbits(31) * random.choice([-1, 1])
    net._vk_method('messages.send', user_tgid, params)


def vk_person_name(vk_id: int):
    user_tgid = user_by_vkid(vk_id)['tgid']
    # Person can be a human or community
    if vk_id > 0:
        resp = net._vk_method('users.get', user_tgid, {
            'user_ids': vk_id
        })['response'][0]
        return resp['first_name'] + ' ' + resp['last_name']
    else:
        return net._vk_method('groups.getById', user_tgid, {
            'group_ids': -vk_id
        })['response'][0]['name']


def vk_msg_attachments(message_id: int, user_tgid: int):
    resp = net._vk_method('messages.getById', user_tgid, {
        'message_ids': message_id
    })
    if resp['response']['items'] == []:
        return 'NO_ATTACHMENTS'

    attachment_type = resp['response']['items'][0]['attachments'][0]['type']
    if attachment_type != 'photo':
        return f'UNSUPPORTED ATTACHMENT_TYPE f{attachment_type}'

    attachments_list = resp['response']['items'][0]['attachments']
    attachments_urls = []

    for attachment in attachments_list:
        attachment_sizes = attachment[attachment_type]['sizes']
        largest_height = 0
        largest_url = ''
        for size in attachment_sizes:
            if size['height'] > largest_height:
                largest_height = size['height']
                largest_url = size['url']
        
        attachments_urls.append(largest_url)

    return [('photo', attachments_urls)]
