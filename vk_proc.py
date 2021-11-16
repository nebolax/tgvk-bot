def single_vk_update(update: list):
    match(update[0]):
        case 4:
            vk_peer = update[3]
            text = update[6]
            tg_method('sendMessage', {
                'chat_id': g_data.vk_roads[vk_peer],
                'text': text
            })
