from . import network as net
import random
import g


def send_vk_message(route: dict, params: dict):
    user_tgid = route['tg_userid']
    params['peer_id'] = route['vk_peer']
    params['random_id'] = random.getrandbits(31) * random.choice([-1, 1])
    net._vk_method('messages.send', user_tgid, params)


def vk_person_name(vk_id: int, requester_tgid: int):
    vk_id = int(vk_id)
    g.logs.debug(f'Vk id: {vk_id}')
    user_tgid = requester_tgid
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
    attachments = []

    for attachment in attachments_list:
        attachment_sizes = attachment[attachment_type]['sizes']
        largest_height = 0  
        largest_url = ''
        for size in attachment_sizes:
            if size['height'] > largest_height:
                largest_height = size['height']
                largest_url = size['url']

        attachments.append(('photo', largest_url))

    return attachments
