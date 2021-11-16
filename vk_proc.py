import g
import api


@g.ee.on('vk.msg')
def single_vk_update(update: list):
    g.logs.debug(update)
    if g.vk_route(update[2]) is None:
        g.logs.debug(f'Got vk-message from unsupported route: {update}')
        return
    
    vk_peer = update[2]
    text = update[5]
    extra_info = update[6]
    sender_id = vk_peer if g.chat_type(vk_peer) == g.RouteType.personal else int(extra_info['from'])

    if sender_id == g.my_vkid:
        g.logs.debug('Got vk message from me')
        return

    api.send_tg_message(g.vk_route(vk_peer),
                        text=f'<b>{api.person_name(sender_id)}:</b>\n' + text
                        )
