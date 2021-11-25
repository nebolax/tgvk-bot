import store

_events_routes = {}

def on(key: str):
    def args_wrap(func):
        _events_routes[key] = func
        return func
    
    return args_wrap

def emit(key: str, *args, **kwargs):
    if key not in _events_routes:
        raise Exception(f'There is no registered observer for event {key}')
    _events_routes[key](*args, **kwargs)
    store.commit()