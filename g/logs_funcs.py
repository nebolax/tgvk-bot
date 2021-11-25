import traceback
from .conf_logs import logs

def tryexcept(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except Exception as e:
            logs.error(
                f'Totally failed to run method {func.__name__}. Args: {args}, {kwargs}. Exception: {e} {traceback.format_exc()}')
    return wrapper