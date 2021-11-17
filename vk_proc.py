import g
import api


@g.ee.on('vk.msg')
def single_vk_update(update: list):
    g.logs.debug(update)
    if g.vk_route(update[2]) is None:
        g.logs.debug(f'Got vk-message from unsupported route: {update}')
        return
    
    flags = "{0:10b}".format(update[1])[::-1][:10]
    g.logs.debug('*' + flags + '*')
    vk_peer = update[2]
    topic = update[4]
    text = update[5]
    extra_info = update[6]
    sender_id = vk_peer if g.chat_type(vk_peer) != g.RouteType.group else int(extra_info['from'])

    if flags[1] == '1':
        g.logs.debug('Got vk message from me')
        return

    api.send_tg_message(g.vk_route(vk_peer),
                        text=f'<b>{api.person_name(sender_id)}:</b>\n' + text
                        )