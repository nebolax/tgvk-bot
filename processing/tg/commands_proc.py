import store


def bot_command(cmd: str, text_args: str, msg: dict):
    match(cmd):
        case 'vkpeer':
            proc_vkpeer_command(text_args, msg)

def proc_start_command(msg: dict):
    if msg['chat']['type'] != 'private':
        return


def proc_vkpeer_command(text_args: str, msg: dict):
    cmd_type, s_peer = text_args.split()
    vk_peer = int(s_peer)

    match(cmd_type):
        case 'личный':
            pass
        case 'беседа':
            vk_peer += 2000000000

    store.new_route(msg['chat']['id'], vk_peer, msg['from']
                    ['id'], store.user_by_tgid(msg['from']['id'])['vkid'])
