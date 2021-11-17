from . import network as net
import g
import random
import requests
import os


def send_vk_message(peer_id: int, params: dict):
    params['peer_id'] = peer_id
    params['random_id'] = random.getrandbits(31) * random.choice([-1, 1])
    net._vk_method('messages.send', params)


def person_name(vk_id: int):
    # Person can be a human or community
    if vk_id > 0:
        resp = net._vk_method('users.get', {
            'user_ids': vk_id
        })['response'][0]
        return resp['first_name'] + ' ' + resp['last_name']
    else:
        return net._vk_method('groups.getById', {
            'group_ids': -vk_id
        })['response'][0]['name']


def message_attachments(message_id: int):
    resp = net._vk_method('messages.getById', {
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

    return attachments_urls
