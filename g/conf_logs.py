import logging

#Инициализация логгера 

logs = logging.getLogger("tgvk-bot")
_uform = f"%(asctime)s-%(levelname)s:%(filename)s.%(funcName)s.%(lineno)d - %(message)s"
_level = logging.DEBUG

logs.setLevel(_level)

_stream_handler = logging.StreamHandler()
_file_handler = logging.FileHandler('logs.txt', 'wt')

_stream_handler.setFormatter(logging.Formatter(_uform))
_file_handler.setFormatter(logging.Formatter(_uform))

logs.addHandler(_stream_handler)
logs.addHandler(_file_handler)
