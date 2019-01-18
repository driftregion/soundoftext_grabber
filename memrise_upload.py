#!/usr/bin/python3

import requests
import os
import sys

URL_BASE = "https://memrise.com/"
URL_LOGIN = URL_BASE + "login/"
URL_COURSE = URL_BASE + "course/1186221/nk-zhong-wen-ci-hui/"
MEMRISE_USERNAME = os.environ["MEMRISE_USERNAME"]
MEMRISE_PASSWORD = os.environ["MEMRISE_PASSWORD"]

if not MEMRISE_USERNAME:
    print("No MEMRISE_USERNAME found in environment, enter it here:")
    MEMRISE_USERNAME = sys.stdin.readline()

client = requests.Session()
client.get(URL_LOGIN)

client.post(
    URL_LOGIN,
    data={
        "username": MEMRISE_USERNAME,
        "password": MEMRISE_PASSWORD,
        "csrfmiddlewaretoken": client.cookies["csrftoken"],
    },
)

response = client.get(URL_COURSE)

import ipdb

ipdb.set_trace()

