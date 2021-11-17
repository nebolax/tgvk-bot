import g, utils
import api
import os


@g.ee.on('vk.msg')
@utils.tryexcept
def single_vk_update(update: list):
    g.logs.debug(update)
    if g.vk_route(update[2]) is None:
        g.logs.warning(f'Got vk-message from unsupported route')
        return

    flags = "{0:10b}".format(update[1])[::-1][:10]
    g.logs.debug('*' + flags + '*')
    msg_id = update[0]
    vk_peer = update[2]
    topic = update[4]
    text = update[5]
    extra_info = update[6]
    sender_id = vk_peer if g.chat_type(
        vk_peer) != g.RouteType.group else int(extra_info['from'])

    if flags[1] == '1':
        g.logs.debug('Got vk message from me')
        return

    if 'attach1' in extra_info:
        g.logs.debug('Got message with attachments')

        attachments_result = api.message_attachments(msg_id)
        if type(attachments_result) == list:
            attaches_tosend = []
            for link in attachments_result:
                attaches_tosend.append({
                    'type': 'photo',
                    'media': link
                })

            api.send_tg_photos(g.vk_route(vk_peer), {
                'media': attaches_tosend
            }, text)
        else:
            g.logs.debug(f'Failed on downloading attachments. Code {attachments_result}')

    else:
        api.send_tg_message(g.vk_route(vk_peer), {
            'text': f'<b>{api.person_name(sender_id)}:</b>\n' + text
        })        
