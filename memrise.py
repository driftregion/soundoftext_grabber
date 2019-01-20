#!/usr/bin/python3

import requests
import os
import sys
import logging

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys


URL_BASE = "https://memrise.com/"
URL_LOGIN = URL_BASE + "login/"
URL_COURSE = URL_BASE + "/course/2193093/zhong-wen-sentence-review/"
URL_COURSE_EDIT = URL_COURSE + "edit/"
MEMRISE_USERNAME = os.environ["MEMRISE_USERNAME"]
MEMRISE_PASSWORD = os.environ["MEMRISE_PASSWORD"]

assert MEMRISE_PASSWORD and MEMRISE_USERNAME

logger = logging.getLogger(__name__)


class Memrise(object):
    def __init__(self):
        self.opts = Options()
        self.opts.set_headless()
        assert self.opts.headless  # Operating in headless mode
        self.browser = Firefox(options=self.opts)
        self.login()

    def login(self):
        self.browser.get(URL_LOGIN)
        self.browser.find_element_by_name("username").send_keys(MEMRISE_USERNAME)
        self.browser.find_element_by_name("password").send_keys(MEMRISE_PASSWORD)
        self.browser.find_element_by_xpath(
            "/html/body/div[7]/div/div[2]/div/div/div/form/input[3]"
        ).send_keys(Keys.RETURN)
        logger.info("login successful")

    browser.get(URL_COURSE_EDIT)

    things = browser.find_elements_by_class_name("things")
    for thing in things:
        wrappers = thing.find_elements_by_class_name("wrapper")
        print([wrapper.text for wrapper in wrappers])

    import ipdb

    ipdb.set_trace()

    search_form = browser.find_element_by_id("search_form_input_homepage")
    search_form.send_keys("real python")
    search_form.submit()
    results = browser.find_elements_by_class_name("result")
    print(results[0].text)

