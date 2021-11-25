import store
from threading import Thread

def func(tg_id: int):
    store.new_user(store.User(tg_id, 2, "abc"))
    store.commit()

t1 = Thread(target=func, args=(12,))
t2 = Thread(target=func, args=(13,))
t1.start()
t2.start()
t1.join()
t2.join()