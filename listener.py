import requests
import time
import configparser

from converter import check

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['TELEGRAM']['api_key']
last_served_request = int(config['TELEGRAM']['last_served_request'])
# last_served_request = int(last_served_request)

url = 'https://api.telegram.org/bot' + api_key
# last_served_request = 199628818

def send_msg(text, chat_id):
    sending_url = url + '/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(sending_url, params = payload)


while True:
    updates_url = url + '/getUpdates'
    payload = {'offset':last_served_request, 'allowed_updates':['message']}
    r = requests.get(updates_url, params=payload)
    data = r.json()['result']
    for x in data:
        print(last_served_request)
        if x['update_id'] <= last_served_request:
            print('ignored')            
        elif 'message' in x:
            print('Chat ID: ' + str(x['message']['chat']['id']))
            print('Text: ' + x['message']['text'])
            print('Update ID: ' + str(x['update_id']))

            msg = check(x['message']['text'])
            chat_id = x['message']['chat']['id']      
            if msg:      
                print(msg)
                send_msg(msg, chat_id)

            last_served_request = x['update_id']
            config['TELEGRAM']['last_served_request'] = str(last_served_request)
            with open('config.ini', 'r+') as configfile:
                config.write(configfile)

    print(last_served_request)
    time.sleep(1)

            

