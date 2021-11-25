import api
import g
from store.images import Route
from .utils import VKMessage


def route_vkmsg(route: Route, msg: VKMessage):
    msg.text = f'<b>{api.vk_person_name(msg.sender_vkid, route.user())}:</b>\n' + msg.text
    attachments = []
    if 'attach1' in msg.extra_info:
        fetched = api.vk_msg_attachments(
            msg.msg_id, route.user())
        attachments = list(map(wrap_attachment_to_send, fetched))

    if len(attachments) == 0:
        api.send_tg_message(route.tg_chat_id, {
            'text': msg.text
        })
    else:
        api.send_tg_media(route.tg_chat_id, msg.text, {'media': attachments})


def wrap_attachment_to_send(attachment: list):
    return {
        'type': attachment[0],
        'media': attachment[1]
    }
