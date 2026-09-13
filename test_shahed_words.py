import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "shahed"})

cands = [
    "tail",
    "self",
    "self_signed",
    "self-signed",
    "self_sign",
    "self-sign",
    "selfsigned",
    "certificate",
    "cert",
    "shahed",
    "rubah",
    "witness"
]

for cand in cands:
    flag = f"YEK{{{cand}}}"
    print(f"Testing {flag}...")
    while True:
        r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag})
        res = r.json()
        if "زیادی تند" in res.get("error", ""):
            time.sleep(6)
            continue
        if res.get("correct"):
            print(f"\n\n🎉🎉🎉 FOUND SHAHED FLAG: {flag} -> {res} 🎉🎉🎉\n\n")
            exit(0)
        else:
            print(f"Failed {flag}: {res.get('message')}")
            break
    time.sleep(10)
