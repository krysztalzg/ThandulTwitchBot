from dotenv import load_dotenv
from os import  environ
from requests import get
from time import sleep

load_dotenv()
delay = environ.get('DELAY', 1)
channel_name = environ.get('CHANNEL', '')
data_url = f'http://89.66.183.3:51300/json/{channel_name}'

while True:
    try:
        data = get(data_url)
        with open('pomoboard.txt', "w", encoding='utf-8') as f:
            f.writelines(data.text)
        sleep(delay)
    except:
        continue
