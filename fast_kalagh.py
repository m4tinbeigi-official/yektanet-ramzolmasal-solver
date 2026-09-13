import subprocess
import requests
import http.cookiejar

def solve(cookie_file):
    session = requests.Session()
    cj = http.cookiejar.MozillaCookieJar(cookie_file)
    cj.load(ignore_discard=True, ignore_expires=True)
    session.cookies = cj

    r = session.get("https://256.yektanet.tech/ramzolmasal/api/kalagh")
    current = r.json()
    print("Start:", current)
    
    while True:
        if isinstance(current, dict) and ("flag" in current or "YEK{" in str(current)):
            print("FOUND FLAG IN KALAGH:", current)
            return current
        shomare = current.get("shomare")
        payam = current.get("payam")
        if shomare is None or payam is None:
            print("Done:", current)
            return current

        # call fast_nonce
        out = subprocess.check_output(["/Users/ricksabchez/workspace/fast_nonce", payam]).decode().strip()
        resp = session.post("https://256.yektanet.tech/ramzolmasal/api/kalagh", json={"shomare": shomare, "nonce": out})
        current = resp.json()
        print(f"Kalagh {shomare} -> nonce {out} -> {current}")

if __name__ == "__main__":
    solve("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
