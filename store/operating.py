from .images import Base
from sqlalchemy.orm import sessionmaker, scoped_session, session
from sqlalchemy import create_engine

sql: scoped_session = None

def init_database():
    user, pwd, host, port, dbname = 'nebolax Star1569 mydb.cnrri9sfbvjr.eu-west-2.rds.amazonaws.com 3306 develop_db'.split()

    engine = create_engine(f'mysql://{user}:{pwd}@{host}:{port}/{dbname}')
    Base.metadata.create_all(engine)

    global sql
    session_factory = sessionmaker(bind=engine)
    sql = scoped_session(session_factory)
    
    print(f'db inited {sql}')

init_database()