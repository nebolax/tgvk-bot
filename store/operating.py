from sqlalchemy.orm import sessionmaker, scoped_session, session
from sqlalchemy import create_engine

import g

_SessionsManager: scoped_session = None
def get_session() -> session.Session:
    return _SessionsManager()

from .images import Base

def _init_operating():
    user, pwd, host, port, dbname = input(
        'Enter database credentials:').split()
    g.logs.info('Initializing db...')

    engine = create_engine(f'mysql://{user}:{pwd}@{host}:{port}/{dbname}')
    Base.metadata.create_all(engine)

    global _SessionsManager
    session_factory = sessionmaker(bind=engine)
    _SessionsManager = scoped_session(session_factory)


#Работает долго! (минимум 1.5 секунды)
def commit():
    print('called')
    _SessionsManager().commit()
    _SessionsManager.remove()


