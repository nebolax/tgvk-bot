from . import network as net
import g
import random


def send_vk_message(peer_id: int, **params: dict):
    params['peer_id'] = peer_id
    params['random_id'] = random.getrandbits(31) * random.choice([-1, 1])
    net._vk_method('messages.send', params)

def person_name(vk_id: int):
    #Person can be a human or community
    if vk_id > 0:
        resp = net._vk_method('users.get', {
            'user_ids': vk_id
        })['response'][0]
        return resp['first_name'] + ' ' + resp['last_name']
    else:
        return net._vk_method('groups.getById', {
            'group_ids': -vk_id
        })['response'][0]['name']
