import json
import enum
from threading import Lock


# class SavingDict(dict):
#     def __init__(self, path: str):
#         self.path = 'json/' + path
#         with open(self.path) as f:
#             loaded = json.loads(f.read())
#             super(SavingDict, self).__init__(loaded)

#     def __setitem__(self, item, value):
#         super(SavingDict, self).__setitem__(item, value)
#         with open(self.path, 'w') as f:
#             f.write(json.dumps(self))

#     def __getitem__(self, key):
#         try:
#             return super().__getitem__(key)
#         except:
#             return None


def dict_to_str(data, tabs=0):
    if type(data) == dict:
        s = '\n'
        for key, val in data.items():
            s += ' '*tabs + key + ': ' + dict_to_str(val, tabs=tabs+2) + '\n'

        return s[:-1] + ' }'

    elif type(data) == list:
        s = '\n'
        for el in data:
            s += ' '*tabs + '{ ' + dict_to_str(el, tabs+2) + ' }\n'
        return s[:-1]
    else:
        return str(data)    

_mutexes = {}
def sync_thread(func, sync_id: str):
    if sync_id not in _mutexes:
        _mutexes[sync_id] = Lock()

    def wrapper(*args, **kwargs):
        with _mutexes[sync_id]:
            func(*args, **kwargs)
        
    return wrapper