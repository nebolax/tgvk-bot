import json

_tokens = {}

def get_vktoken(tg_userid):
    tg_userid = str(tg_userid)
    if tg_userid not in _tokens:
        return None
    
    return _tokens[tg_userid]

def set_vktoken(tg_userid, token: str):
    tg_userid = str(tg_userid)
    _tokens[tg_userid] = token
    with open('tokens.json', 'w') as f:
        f.write(json.dumps(_tokens))

def getall_tgusers() -> list[str]:
    return _tokens.keys()

def _init():
    global _tokens
    with open('tokens.json') as f:
        _tokens = json.loads(f.read())

_init()