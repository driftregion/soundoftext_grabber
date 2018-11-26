#!/usr/bin/python3

import requests
import threading
import argparse
import os
import time

URL_BASE = "https://api.soundoftext.com/"
DOWNLOADS_DIRECTORY = os.path.join(os.path.expanduser("~"), "Downloads")


def get_request_body(text=""):
    return {
        "engine": "Google",
        "data": {
            "text": text,
            "voice": "cmn-Hant-TW"
        }
    }

def fetch(text=""):
    print(f"fetching {text}")
    body = get_request_body(text)
    res = requests.post(URL_BASE + 'sounds/', json=body)
    if res.status_code != 200:
        return
    res = requests.get(URL_BASE + 'sounds/' + res.json()['id'])
    time.sleep(1)    
    res = requests.get(res.json()['location'])
    with open(f'{DOWNLOADS_DIRECTORY}/{text}.mp3', 'wb') as sound:
        sound.write(res.content)
    print("done")

parser = argparse.ArgumentParser()
parser.add_argument('text', nargs=1, default='', type=str, help="A string of words, space or comma separated, e.g. '中文 练习 下雪")
args = parser.parse_args()

fetch(args.text[0])