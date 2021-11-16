

def send_tg_message(chat_id: int, text: str):
    _tg_method('sendMessage', {
        'chat_id': chat_id,
        'text': text
    })