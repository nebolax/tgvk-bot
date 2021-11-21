import g
import store
from . import *


@g.ee.on('vk.msg')
def new_vk_message(inp_msg: list):
    obj_msg = {
        'flags': '{0:10b}'.format(inp_msg[1])[::-1][:10],
        'msg_id': inp_msg[0],
        'peer': inp_msg[2],
        'topic': inp_msg[4],
        'text': inp_msg[5],
        'extra_info': inp_msg[6],
    }
    obj_msg['text'] = obj_msg['text'].replace('<br>', '\n')

    all_connected_routes = store.routes_by_vkpeer(obj_msg['peer'])
    for route in all_connected_routes:
        if route['chat_type'] == 'group':
            obj_msg['sender_id'] = obj_msg['extra_info']['from']
        else:
            if obj_msg['flags'][1] == '1':
                obj_msg['sender_id'] = route['vk_userid']
            else:
                obj_msg['sender_id'] = obj_msg['peer']

        if route['vk_userid'] != obj_msg['sender_id']:
            route_vkmsg(route, obj_msg)
