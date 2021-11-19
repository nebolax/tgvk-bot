import g
import traceback

def tryexcept(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            g.logs.error(
                f'Totally failed to process message {e} {traceback.format_exc()}')
    return wrapper