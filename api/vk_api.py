from store import User, Route
import store
from . import network as net
import random
import g


def send_vk_message(route: Route, params: dict):
    params['peer_id'] = route.vk_peer
    params['random_id'] = random.getrandbits(31) * random.choice([-1, 1])
    net._vk_method('messages.send', route.user.vk_token, params)


def vk_people_name(user_ids: list[int], req_user: User):
    if type(user_ids) == int:
        user_ids = [user_ids]

    # Person can be a human or community
    res = []

    users = list(filter(lambda x: x > 0, user_ids))
    groups = []
    groups_inds = []
    for i, el in enumerate(user_ids):
        if el < 0:
            groups.append(-el)
            groups_inds.append(i)
    print('****', groups)

    if len(users) > 0:
        resp = net._vk_method('users.get', req_user.vk_token, {
            'user_ids': ','.join(list(map(lambda x: str(x), users)))
        })['response']
        res += list(map(lambda x: x['first_name']+' '+x['last_name'], resp))
    if len(groups) > 0:
        resp = net._vk_method('groups.getById', req_user.vk_token, {
            'group_ids': ','.join(list(map(lambda x: str(x), groups)))
        })['response']
        for ind, el in zip(groups_inds, list(map(lambda x: x['name'], resp))):
            res.insert(ind, el)

    return res

def vk_msg_attachments(message_id: int, req_user: User):
    resp = net._vk_method('messages.getById', req_user.vk_token, {
        'message_ids': message_id
    })
    if resp['response']['items'] == []:
        return 'NO_ATTACHMENTS'

    attachment_type = resp['response']['items'][0]['attachments'][0]['type']
    if attachment_type != 'photo':
        return f'UNSUPPORTED ATTACHMENT_TYPE f{attachment_type}'

    attachments_list = resp['response']['items'][0]['attachments']
    attachments = []

    for attachment in attachments_list:
        attachment_sizes = attachment[attachment_type]['sizes']
        largest_height = 0
        largest_url = ''
        for size in attachment_sizes:
            if size['height'] > largest_height:
                largest_height = size['height']
                largest_url = size['url']

        attachments.append(('photo', largest_url))

    return attachments

def get_conversations(user: User, count: int, offset: int) -> list[store.VkConversation]:
    resp = net._vk_method('messages.getConversations', user.vk_token, {
        'offset': offset,
        'count': count
    })
    conversations = []
    req_user_names = []
    inp_items = resp['response']['items']
    for inp_item in inp_items:
        inp_conv = inp_item['conversation']

        chat_type = store.ChatType.Group
        vk_peer = inp_conv['peer']['id']

        if inp_conv['peer']['type'] in {'user', 'group'}:
            chat_type = store.ChatType.Private
        
        try:
            title = ''
            if chat_type == store.ChatType.Group:
                title = inp_conv['chat_settings']['title']
            else:
                # title = vk_person_name(vk_peer, user)
                req_user_names.append([vk_peer, len(conversations)])
            conversations.append(store.VkConversation(vk_peer, title, chat_type))
        except Exception as e:
            g.logs.error(f'{e}  **   {inp_conv}')

    ans = vk_people_name(list(zip(*req_user_names))[0], user)
    fetched_names = list(zip(ans, list(zip(*req_user_names))[1]))
    for fn in fetched_names:
        conversations[fn[1]].title = fn[0]
    # g.logs.debug(list(map(lambda x: x.title, conversations)))
    # with open('f.txt', 'w') as f:
    #     f.write(g.dict_to_str(conversations))

    print(conversations)
    return conversations