#!/usr/bin/python3

import requests
import os
import time
import json
import logging
import sys

URL_BASE = "https://api.soundoftext.com/"
DOWNLOADS_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")


logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(0)


def get_request_body(text=""):
    return {"engine": "Google", "data": {"text": text, "voice": "cmn-Hant-TW"}}


def fetch_phrase(text=""):
    try:
        os.mkdir(DOWNLOADS_DIRECTORY)
    except:
        pass
    logger.info(f"fetching {text}")
    body = get_request_body(text)
    res = requests.post(URL_BASE + "sounds/", json=body)
    if res.status_code != 200:
        return
    res = requests.get(URL_BASE + "sounds/" + res.json()["id"])
    time.sleep(1)
    try:
        res = requests.get(res.json()["location"])
    except KeyError:
        import ipdb

        ipdb.set_trace()

    sound_path = f"{DOWNLOADS_DIRECTORY}/{text}.mp3"
    with open(sound_path, "wb") as sound:
        sound.write(res.content)
    logger.info(f"saved to: {sound_path}")
    return sound_path

