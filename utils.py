import g
import traceback

class Singleton(type):
    def __init__(self, *args, **kwargs):
        super(Singleton, self).__init__(*args, **kwargs)
        self.__instance = None
    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.__instance

class ObservableDict(dict):
    def __init__(self, onchange_method, *args, **kwargs):
        super(ObservableDict, self).__init__(*args, **kwargs)
        print(type(onchange_method))
        if type(onchange_method).__name__ != 'function':
            raise Exception('Processing function is not callable!!')
        self.onchange_method = onchange_method

    def __setitem__(self, item, value):
        super(ObservableDict, self).__setitem__(item, value)
        self.onchange_method(self)

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except:
            return None

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

def tryexcept(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            g.logs.error(f'Totally failed to process message {e} {traceback.format_exc()}')
    return wrapper