import json

base_tg_url = 'https://api.telegram.org/'
base_vk_url = 'https://api.vk.com/method/'
with open('json/confidential.json') as f:
    bot_token = json.loads(f.read())['bot_token']

welcome_message = '''
    Привет!
    Я - бот, который позволит тебе не заходить в противный вк,
    а лишь наслаждаться красотой телеграма!
    Пройди по <a href="https://oauth.vk.com/authorize?client_id=2685278&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,messages,offline,docs,photos,video,stories,audio&response_type=token&v=5.131">Этой ссылке</a>, 
    дай разрешение, а затем скопируй адрес страницы в этот чат
'''
