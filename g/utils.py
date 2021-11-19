import json
import enum


class SavingDict(dict):
    def __init__(self, path: str):
        with open(path) as f:
            loaded = json.loads(f.read())
            super(SavingDict, self).__init__(loaded)
        self.path = 'json/' + path

    def __setitem__(self, item, value):
        super(SavingDict, self).__setitem__(item, value)
        with open(self.path, 'w') as f:
            f.write(json.dumps(self))

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except:
            return None


class RouteType(enum.Enum):
    personal = 0
    group = 1
    community = 2


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
