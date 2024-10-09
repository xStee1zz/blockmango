import random
import threading

import requests

response = requests.get('https://raw.githubusercontent.com/xStee1zz/nebeta/refs/heads/main/bot.txt')
bots = response.text.splitlines()

data = {
    'friendId': 2801613998,
    'msg': ''
}

session = requests.Session()

def friends():
    while True:
        bot = random.choice(bots).strip()
        try:
            bot_id, bot_token = bot.split(':')
        except ValueError:
            continue

        url = "https://gw.sandboxol.com/friend/api/v1/friends"

        headers = {
            'userId': bot_id,
            'Access-Token': bot_token,
            'User-Agent': 'okhttp/3.12.1'
        }

        response = session.post(url, headers=headers, json=data)
        print(response.text)

threads = []
for _ in range(5000):
    t = threading.Thread(target=friends)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
