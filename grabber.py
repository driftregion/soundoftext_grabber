#!/usr/bin/python3

import requests
import os
import time
import json
import logging
import sys

URL_BASE = "https://api.soundoftext.com/"
DOWNLOADS_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")
PHRASES_JSON_NAME = "phrases.json"

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
    logger.info(f"fetching {text}", end=" ... ")
    body = get_request_body(text)
    res = requests.post(URL_BASE + "sounds/", json=body)
    if res.status_code != 200:
        return
    res = requests.get(URL_BASE + "sounds/" + res.json()["id"])
    time.sleep(1)
    res = requests.get(res.json()["location"])
    sound_path = f"{DOWNLOADS_DIRECTORY}/{text}.mp3"
    with open(sound_path, "wb") as sound:
        sound.write(res.content)
    logger.info(f"saved to: {sound_path}")
    return sound_path


def read_phrases_json():
    with open(PHRASES_JSON_NAME, "r") as phrases_json_file:
        phrases = json.load(phrases_json_file)
    return phrases


def write_phrases_json(phrases):
    with open(PHRASES_JSON_NAME, "w") as phrases_json_file:
        json.dump(phrases, phrases_json_file, ensure_ascii=False, indent=2)


def download_phrases():
    phrases = read_phrases_json()
    for phrase in phrases:
        if not phrase["en"]:
            logger.error(f"no 'en' field for phrase {phrase}")
            return
        if phrase.get("path") and os.path.isfile(phrase.get("path")):
            logger.debug(f"phrase {phrase['en']} has already been downloaded")
        else:
            sound_path = fetch_phrase(text=phrase["zh"])
            phrase["path"] = sound_path
        write_phrases_json(phrases)


download_phrases()
