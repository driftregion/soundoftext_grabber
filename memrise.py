#!/usr/bin/python3

import requests
import os
import sys
import logging
import time
from typing import List

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys


URL_BASE = "https://memrise.com/"
URL_LOGIN = URL_BASE + "login/"
URL_COURSE = URL_BASE + "course/2193093/zhong-wen-sentence-review/"
URL_COURSE_EDIT = URL_COURSE + "edit/"

URL_AJAX_ADD = "https://www.memrise.com/ajax/level/thing/add/"

MEMRISE_USERNAME = os.environ["MEMRISE_USERNAME"]
MEMRISE_PASSWORD = os.environ["MEMRISE_PASSWORD"]

assert MEMRISE_PASSWORD and MEMRISE_USERNAME

logger = logging.getLogger(__name__)


class Thing(object):
    """
    Represents a "thing" in Memrise's course editing page
    """

    def __init__(self, element):
        self.element = element

    @property
    def zh(self):
        return self.element.find_elements_by_class_name("wrapper")[0].text

    @property
    def en(self):
        return self.element.find_elements_by_class_name("wrapper")[1].text

    @property
    def already_has_audio(self):
        return (
            self.element.find_element_by_xpath(".//td[@data-key='4']//div//button").text
            != "no audio file"
        )

    def add_audio(self, audio_file):
        upload_element = self.element.find_element_by_xpath(
            ".//td[@data-key='4']//div//div//input"
        )
        upload_element.send_keys(audio_file)


class Memrise(object):
    def __init__(self):
        self.opts = Options()
        # self.opts.set_headless()
        # assert self.opts.headless  # Operating in headless mode
        self.browser = Firefox(options=self.opts)

    def login(self):
        self.browser.get(URL_LOGIN)
        self.browser.find_element_by_name("username").send_keys(MEMRISE_USERNAME)
        self.browser.find_element_by_name("password").send_keys(MEMRISE_PASSWORD)
        self.browser.find_element_by_xpath("//*[@value='Login']").click()
        self.browser.get(URL_COURSE_EDIT)

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()

    def get_things(self) -> List[Thing]:
        thing_elements = self.browser.find_elements_by_xpath(
            "//tbody[@class='things']//tr[@class='thing']"
        )
        return [Thing(element) for element in thing_elements]

    def add_thing(self, en, zh):
        fields = self.browser.find_elements_by_xpath(
            ".//tr[@data-role='add-form']//td//input"
        )

        # fields[0].click()
        fields[0].send_keys(zh)
        # fields[1].send_keys(Keys.TAB)
        fields[1].send_keys(en)
        fields[1].send_keys(Keys.RETURN)

        time.sleep(1)  # :(
