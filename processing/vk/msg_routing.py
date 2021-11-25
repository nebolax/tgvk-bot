import g, events
import store
from store.images import ChatType, User
from . import *
from dataclasses import dataclass
from .utils import VKMessage
from .msg_proc import route_vkmsg

@events.on('vk.msg')
def new_vk_message(inp_msg: list):
    obj_msg = VKMessage(
        flags='{0:10b}'.format(inp_msg[1])[::-1][:10],
        msg_id=inp_msg[0],
        peer=inp_msg[2],
        topic=inp_msg[4],
        text=inp_msg[5],
        extra_info=inp_msg[6],
        sender_vkid=None
    )
    obj_msg.text = obj_msg.text.replace('<br>', '\n')

    all_connected_routes = store.routes_by_vkpeer(obj_msg.peer)
    
    for route in all_connected_routes:
        g.logs.debug(f'{route.__dict__}')
        if route.chat_type == ChatType.Group:
            obj_msg.sender_vkid = int(obj_msg.extra_info['from'])
        else:
            if obj_msg.flags[1] == '1':
                obj_msg.sender_vkid = route.user().vk_id
            else:
                obj_msg.sender_vkid = obj_msg.peer
        g.logs.debug(route.user().__dict__)
        if route.user().vk_id != obj_msg.sender_vkid:
            route_vkmsg(route, obj_msg)
