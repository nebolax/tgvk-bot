# import re
# import g
# import api, store

# def exec_tg_command(cmd: str, text: str, message: dict):
#     match(cmd):
#         case '/vkpeer':
#             t, s_peer = text.split()
#             vk_peer = int(s_peer)
#             match(t):
#                 case 'p':
#                     pass
#                 case 'g':
#                     vk_peer += 2000000000
#                 case 'c':
#                     vk_peer *= -1
#                 case _:
#                     g.logs.warning(
#                         f'Got unsupported chat type in command {cmd} of message {message}')
#                     raise Exception()
#             g.set_route(int(message['chat']['id']), vk_peer)
#         case '/start':
#             g.logs.debug(message)
#             if message['chat']['type'] == 'private':
#                 if message['chat']['id'] not in g.state['waiting_for_token']:
#                     g.state['waiting_for_token'].append(message['chat']['id'])
#                 api.send_tg_message(message['chat']['id'], {'text': static_info.welcome_message})


# @g.ee.on('tg.msg')
# @utils.tryexcept
# def proc_tg_message(message: dict):
#     g.logs.debug(f"Got telegram-message from: {message['from']['id']}")
#     if message['chat']['id'] in g.state['waiting_for_token']:
#         vk_token_search = re.search(r'access_token=(.+?)&', message['text'])
#         if vk_token_search is None:
#             api.send_tg_message(message['chat']['id'], {'text': 'Некорректная ссылка. Попробуйте еще раз'})
#             return
#         vk_token = vk_token_search.group(1)
#         security.set_vktoken(message['from']['id'], vk_token)
#         api.start_new_vklongpoll(message['from']['id'])
#         api.send_tg_message(message['chat']['id'], {'text': 'Поздравляю с успешной авторизацией!'})
#     # if 'entities' in message:
#     #     for entity in message['entities']:
#     #         if entity['type'] == 'bot_command':
#     #             if entity['offset'] != 0:
#     #                 print('ignoring command')
#     #             else:
#     #                 cmd = message['text'][:entity['length']]
#     #                 text = message['text'][entity['length']:].strip()
#     #                 try:
#     #                     exec_tg_command(cmd, text, message)
#     #                 except Exception as e:
#     #                     g.logs.warning(
#     #                         f'Command {cmd} of message  failed! {message}\n Exception: {e}')
#     #                     api.send_tg_message(message['chat']['id'],
#     #                                         {'text': 'Your last command has failed'})
#     elif 'photo' in message:
#         g.logs.debug(message['photo'])
#         photo_link = api.get_tg_photo_link(message['photo'])
#         g.logs.debug(photo_link)

#     else:
#         if g.tg_route(message['chat']['id']) is None:
#             return
#         try:
#             vk_chat_peer = g.tg_route(message['chat']['id'])
#             api.send_vk_message(vk_chat_peer, message['from']['id'], {
#                                 'message': message['text']})
#         except Exception as e:
#             g.logs.warning(f'Cant process message {message}. Error {e}')
#             api.send_tg_message(message['chat']['id'], {
#                                 'text': 'Cant process last message'})
