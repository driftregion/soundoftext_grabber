#!/usr/bin/python3

import json
import logging
import sys
import os
from soundoftext import fetch_phrase
from memrise import Memrise

# from .memrise import Memrise


PHRASES_JSON_NAME = "phrases.json"

logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(0)


class Schema(object):
    def __init__(self):
        self.data = {}
        self.load_from_json()

    def load_from_json(self):
        with open(PHRASES_JSON_NAME, "r") as phrases_json_file:
            self.data = json.load(phrases_json_file)

    def save_to_json(self):
        with open(PHRASES_JSON_NAME, "w") as phrases_json_file:
            json.dump(self.data, phrases_json_file, ensure_ascii=False, indent=2)


s = Schema()


def download_phrases():
    for phrase in s.data["phrases"]:
        if not phrase["en"]:
            logger.error(f"no 'en' field for phrase {phrase}")
            return
        if phrase.get("path") and os.path.isfile(phrase.get("path")):
            logger.debug(f"phrase {phrase['en']} has already been downloaded")
        else:
            sound_path = fetch_phrase(text=phrase["zh"])
            phrase["path"] = sound_path
            s.save_to_json()


download_phrases()

with Memrise() as m:
    phrases = s.data["phrases"]
    for phrase in phrases:
        matching_things = [
            thing for thing in m.get_things() if thing.en == phrase["en"]
        ]
        thing = matching_things[0] if matching_things else None
        if thing:
            logger.info(f"phrase already added: {phrase['en']}")
            if thing.already_has_audio:
                pass
            elif phrase and phrase.get("path"):
                thing.add_audio(phrase["path"])

        else:
            try:
                m.add_thing(phrase["en"], phrase["zh"])
            except Exception:
                import ipdb

                ipdb.set_trace()
