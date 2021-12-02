import g
import store
import api

#Обязательно импортить для регистрации путей ивентов
import processing

if __name__ == '__main__':
    # store.init_database()
    api.init_network()
    g.logs.info('App running...')
