import g, store
from . import *


@g.ee.on('vk.msg')
@tryexcept
def vk_message_update(inp_msg: list):
    obj_update = {
        'flags': '{0:10b}'.format(inp_msg[1])[::-1][:10],
        'msg_id': inp_msg[0],
        'peer': inp_msg[2],
        'topic': inp_msg[4],
        'text': inp_msg[5],
        'extra_info': inp_msg[6],
    }
    obj_update['sender_id'] = obj_update['peer'] if g.chat_type(
        obj_update['peer']) != g.RouteType.group else int(obj_update['extra_info']['from'])

    all_connected_routes = store.routes_by_vkpeer(obj_update['peer'])

    for route in all_connected_routes:
        if route['vk_userid'] != obj_update['sender_id']:
            route_vkmsg(route, obj_update)
    # ###########################################################################
    # if 'attach1' in extra_info:
    #     g.logs.debug('Got message with attachments')

    #     attachments_result = api.message_attachments(msg_id)
    #     if type(attachments_result) == list:
    #         attaches_tosend = []
    #         for link in attachments_result:
    #             attaches_tosend.append({
    #                 'type': 'photo',
    #                 'media': link
    #             })

    #         api.send_tg_media(g.vk_route(vk_peer), {
    #             'media': attaches_tosend
    #         }, text)
    #     else:
    #         g.logs.debug(f'Failed on downloading attachments. Code {attachments_result}')

    # else:
    #     api.send_tg_message(g.vk_route(vk_peer), {
    #         'text': f'<b>{api.person_name(sender_id)}:</b>\n' + text
    #     })        
