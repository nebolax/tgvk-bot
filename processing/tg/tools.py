from dataclasses import dataclass
import enum
import store as db


@dataclass
class TgMsgEntity:
    offset: int
    length: int
    type: str


class TgChatType(enum.Enum):
    private = 1
    group = 2


class TgMsg:
    id: int
    route: db.Route

    sender: db.User
    text: str

    sender_id: int
    chat_id: int
    chat_type: TgChatType

    entities: list[TgMsgEntity]

    def __init__(self, inp_msg: dict) -> None:
        self.id = int(inp_msg['message_id'])

        self.route = db.sql.query(db.Route).filter(
            db.Route.tg_chat_id == inp_msg['chat']['id']).first()
        self.sender = db.sql.query(db.User).filter(
            db.User.tg_id == inp_msg['from']['id']).first()
        self.text = inp_msg['text']

        self.sender_id = inp_msg['from']['id']
        self.chat_id = inp_msg['chat']['id']

        if inp_msg['chat']['type'] == 'private':
            self.chat_type = TgChatType.private
        else:
            self.chat_type = TgChatType.group

        self.entities = []
        if 'entities' in inp_msg:
            for inp_ent in inp_msg['entities']:
                self.entities.append(TgMsgEntity(
                    inp_ent['offset'], inp_ent['length'], inp_ent['type']))
