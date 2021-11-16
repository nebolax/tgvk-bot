import logging
import pymitter

logs = logging.getLogger("tgvk-bot")

logs.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(
    f"%(levelname)s:%(filename)s.%(funcName)s - %(message)s"
))
logs.addHandler(stream_handler)

ee = pymitter.EventEmitter()

tg_roads = {}
vk_roads = {}

def add_road(tg_chat_id: int, vk_peer: int):
    tg_roads[tg_chat_id] = vk_peer
    vk_roads[vk_peer] = tg_chat_id
    logs.debug(f"Added road: vk_peer {vk_peer} is now connected to {tg_chat_id} telegram chat)")