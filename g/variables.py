import logging
import pymitter
from . import *

# В этом файле находятся глобалальные объекты, требующие инициализации при запуске

logs = logging.getLogger("tgvk-bot")

logs.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('logs/otp.md', 'wt')
stream_handler.setFormatter(logging.Formatter(
    f"%(levelname)s:%(filename)s.%(funcName)s.%(lineno)d - %(message)s"
))
file_handler.setFormatter(logging.Formatter(
    f"%(levelname)s:%(filename)s.%(funcName)s.%(lineno)d - %(message)s"
))
logs.addHandler(stream_handler)
logs.addHandler(file_handler)

ee = pymitter.EventEmitter()

state = SavingDict('state.json')
