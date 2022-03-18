from .images import Base
from sqlalchemy.orm import sessionmaker, scoped_session, session
from sqlalchemy import create_engine
from dotenv import dotenv_values

sql: scoped_session = None


def init_database():
    db_creds = dotenv_values('.env')
    # user, pwd, host, port, dbname = input('Database credentialas:').split()

    engine = create_engine(
        f'mysql://{db_creds["USER"]}:{db_creds["PWD"]}@{db_creds["HOST"]}:{db_creds["PORT"]}/{db_creds["DB_NAME"]}')
    Base.metadata.create_all(engine)

    global sql
    session_factory = sessionmaker(bind=engine)
    sql = scoped_session(session_factory)

    print(f'db inited {sql}')


init_database()
