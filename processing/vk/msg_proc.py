import api, g


def route_vkmsg(route: dict, msg: dict):
    msg['text'] += f'<b>{api.vk_person_name(msg["sender_id"], route["tg_userid"])}:</b>\n'
    attachments = []
    if 'attach1' in msg['extra_info']:
        fetched = api.vk_msg_attachments(
            msg['msg_id'], route['tg_userid'])
        attachments = list(map(wrap_attachment_to_send, fetched))

    if len(attachments) == 0:
        api.send_tg_message(route['tg_chatid'], {
            'text': msg['text']
        })
    else:
        api.send_tg_media(route['tg_chatid'], msg['text'], {'media': attachments})


def wrap_attachment_to_send(attachment: list):
    return {
        'type': attachment[0],
        'media': attachment[1]
    }
