# tgvk-bot

The main purpose of this bot is to provide functionality for user to chat in [vk](https://vk.com) while being in telegram.

Latest version on github may not work so if you want stable release revert to commit 8294492 or earlier

## How this works

1. You authorize into your vk account and give bot permission to read and write messages in vk.
2. You create a group chat in telegram where only members are you and a bot.
3. You tell bot a chat peer (chat id in vk) and type of chat - personal / group.
4. Bot transfers every message from you into vk chat and from vk chat into this telegram group.

### Messages features

- If this is a group chat bot adds name of sender to the message
- Images support
- User-friendly picking of the desired chat when group with bot has been created (but works slow right now)

## Required features

There is a list of features required into bot to make it useful:

- Support of forwarded messages and replies (at least receiveng them from vk)
- Stickers and voice messages support
- Synchronize messages if I chat using vk (not this bot)
- If there is no group in telegram for vk chat, send messages from this chat into personal messages with bot
- Load history of the chat when telegram group is created
- Support of editing messages

## Under the hood

Right now program runs in multithreading (tg_longpoll has personal thread and each vk user has) but I'm not very sure if this system has been working nice and smooth...

###Program consists of several main modules:

- _api_ - this module realizes botapi of telegram through pure python requests module. There are 3 files:
  - network.py - does requests on lowlevel and performs longpolling of vk and telegram bot, if any new events came throws event
  - tg_api.py & vk_api.py - are built on top of network.py and realize methods like "send message to user" in one function
- _g_ - provides global objects like logging, utility functions and static information like base_tg_url of telegram botapi system
- _store_ - module which uses SQLAlchemy and provide methods to save data about messages, routes (connection between vk chat and tg chat) and users in the mysql database (aws rds used)
- _processing_ - does main processing of messages and has 2 submodules - _vk_ and _tg_ which process incoming messages from corresponding platforms. Each submodules has follwing structure:
  - _routing_ - catches events from network.py and decides where should this event go next
  - _msg-proc_ - contains a bunch of methods, each method for specific type of message
  - _tools_ - contains util methods for messages processing and data structures
  - tg submodule has _commands-proc_ file which contains methoda for processing incoming commands from user
- separate file _events.py_ which contains simple events system

## TODO in programming aspect

- Rewrite everything into data structures (at this moment program often uses dictionary structure bevause it receives messages in this format but as program grows such approach becomes unreliable)
- Make program architecture more specific because right now it (especially _processing_ module) is a bit messy and I always doubt in it
- Increase speed. Sometimes bot thinks too much (when scaning user vk chats)...
- Increase security (especially bot_token and users' personal information store). If I want to put this in the production and allow other people to use my bot security must be very high.
