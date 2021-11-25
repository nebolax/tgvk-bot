from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
import enum
from .operating import get_session
from sqlalchemy.orm.session import Session

class ChatType(enum.Enum):
    Private = 0
    Group = 1

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    tg_id = Column(Integer, primary_key=True)
    vk_id = Column(Integer)
    vk_token = Column(String(100))

    def __init__(self, tg_id: int, vk_id: int, vk_token: str):
        self.tg_id = tg_id
        self.vk_id = vk_id
        self.vk_token = vk_token

class Route(Base):
    __tablename__ = 'routes'

    tg_chat_id = Column(Integer, primary_key=True)
    vk_peer = Column(Integer)
    chat_type = Column('chat_type', Enum(ChatType))
    tg_userid = Column(Integer, ForeignKey('users.tg_id'))

    def __init__(self, tg_chat_id: int, vk_peer: int, chat_type: ChatType, tg_userid: int):
        self.tg_chat_id = tg_chat_id    
        self.vk_peer = vk_peer
        self.chat_type = chat_type
        self.tg_userid = tg_userid

    def user(self) -> User:
        return get_session().query(User).filter(User.tg_id == self.tg_userid).first()

class MessageMatch(Base):
    __tablename__ = 'message_matches'

    tg_msg_id = Column(Integer, primary_key=True)
    vk_msg_id = Column(Integer)
    user_id = Column(Integer)

    def __init__(self, tg_msg_id: int, vk_msg_id: int, user_id: int):
        self.tg_msg_id = tg_msg_id
        self.vk_msg_id = vk_msg_id
        self.user_id = user_id