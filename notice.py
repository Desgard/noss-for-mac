import time
import os

from pynostr.key import PrivateKey
from env import private_key, public_key
import requests
import logging

identity_pk = PrivateKey.from_nsec(private_key)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read():
    with open("count.txt", "w+") as file:
        val = file.read().strip()
        if val is None or val == "":
            val = 0
        file.write(str(val))
    return val

def write(val):
    with open("count.txt", "w+") as file:
        file.write(str(val))
    return val

# The notifier function
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

# Calling the function
# notify(title    = 'A Real Notification',
#        subtitle = 'with python',
#        message  = 'Hello, this is me, notifying you!')



while True:
    responses = requests.get("https://api-worker.noscription.org/indexer/balance?npub="+public_key)
    data = responses.json()
    logging.info(data)
    old = read()
    if data[0]['balance'] > old:
        # toaster = ToastNotifier()
        # toaster.show_toast("挖到了！！！", f"新增{data[0]['balance'] - old}个, 总量{data[0]['balance']}", duration=5)
        notify(title    = '挖到了',
               subtitle = 'with python',
               message  = f"新增{data[0]['balance'] - old}个, 总量{data[0]['balance']}")
        write(data[0]['balance'])
        
    time.sleep(10)


