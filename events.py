from threading import Thread
import time
import store as db
import g

_events_routes = {}


def on(key: str):
    def args_wrap(func):
        _events_routes[key] = func
        return func

    return args_wrap


def _event_proc(key: str, args: list, kwargs: dict):
    start = time.time()

    if key not in _events_routes:
        raise Exception(f'There is no registered observer for event {key}')
    _events_routes[key](*args, **kwargs)

    finish = time.time()
    g.logs.info(f'Took {finish - start} to process event')


def emit(key: str, *args, **kwargs):
    new_thread = False
    if not new_thread:
        try:
            _event_proc(key, args, kwargs)
        except Exception as e:
            g.logs.error(f'Error {e} occured while processing event!')
    else:
        tr = Thread(target=_event_proc, args=(key, args, kwargs,))
        tr.start()
