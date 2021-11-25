from dataclasses import dataclass
from store import User

@dataclass
class VKMessage:
    flags: str
    msg_id: int
    peer: int
    topic: str
    text: str
    sender_vkid: int
    extra_info: dict
