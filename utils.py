class Singleton(type):
    def __init__(self, *args, **kwargs):
        super(Singleton, self).__init__(*args, **kwargs)
        self.__instance = None
    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.__instance

def dict_to_str(data, tabs=0):
    if type(data) == dict:
        s = '\n'
        for key, val in data.items():
            s += ' '*tabs + key + ': ' + dict_to_str(val, tabs=tabs+2) + '\n'
        
        return s[:-1]
    else:
        return str(data)