#!/usr/bin/env python3
import time
import json
import requests
import os
import sys

BASE_URL = "https://256.yektanet.tech/ramzolmasal"
COOKIE_FILE = "/Users/ricksabchez/workspace/ramzolmasal_cookies.txt"

session = requests.Session()
if os.path.exists(COOKIE_FILE):
    import http.cookiejar
    cj = http.cookiejar.MozillaCookieJar(COOKIE_FILE)
    cj.load(ignore_discard=True, ignore_expires=True)
    session.cookies = cj

def check_status():
    r = session.get(f"{BASE_URL}/api/status")
    return r.json()

def get_me():
    r = session.get(f"{BASE_URL}/api/me")
    return r.json()

def get_board():
    r = session.get(f"{BASE_URL}/api/board")
    return r.json()

if __name__ == "__main__":
    me = get_me()
    print("User authenticated:", me)
    status = check_status()
    print("Contest Status:", status)
